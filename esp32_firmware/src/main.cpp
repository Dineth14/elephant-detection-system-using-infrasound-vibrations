#include <Arduino.h>
#include <FS.h>
#include <SPIFFS.h>
#include "AudioProcessor.h"
#include "KNNClassifier.h"
#include "SerialProtocol.h"

// Pin definitions
#define MIC_PIN 34         // Analog microphone pin (capacitor/electret mic)
#define MIC_VCC_PIN 33     // Optional: Power pin for microphone (3.3V)

// Audio configuration
#define SAMPLE_RATE 1000      // 1 kHz sampling rate for elephant logger
#define CLASSIFICATION_INTERVAL 256  // ms between classifications (frame size)

// Global objects
AudioProcessor audio_processor;
KNNClassifier classifier;
SerialProtocol serial_protocol;

// Global variables for communication with SerialProtocol
AudioFeatures last_features;
String last_classification = "unknown";
float last_confidence = 0.0;
bool has_new_features = false;

// Timing variables
unsigned long last_classification_time = 0;
unsigned long last_status_print = 0;

// Function prototypes
void init_analog_microphone();
void read_analog_samples();
void process_audio_frame();

void setup() {
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("ESP32 Elephant Logger Starting...");
    
    // Initialize SPIFFS
    if (!SPIFFS.begin(true)) {
        Serial.println("ERROR:SPIFFS initialization failed");
        return;
    }
    
    // Initialize audio processor
    audio_processor.initialize();
    Serial.println("Audio processor initialized (1kHz, 256-sample frames, 10–200Hz focus)");
    
    // Initialize classifier
    classifier.initialize();
    // Try to load existing data
    if (classifier.load_from_storage()) {
        Serial.print("Loaded ");
        Serial.print(classifier.get_sample_count());
        Serial.println(" samples from storage");
    } else {
        Serial.println("No existing data found, starting fresh");
    }
    
    // Initialize serial protocol
    serial_protocol.initialize();
    
    // Initialize audio input
    init_analog_microphone();
    
    Serial.println("Setup complete - ready for operation");
}

void loop() {
    // Handle serial communication
    serial_protocol.handle_input();
    
    // Read audio samples
    read_analog_samples();
    
    // Process audio frame for classification
    process_audio_frame();
    
    // Send periodic status updates
    if (millis() - last_status_print > 5000) {  // Every 5 seconds
        serial_protocol.send_status();
        last_status_print = millis();
    }
}

void init_analog_microphone() {
    // Configure ADC for microphone input
    analogReadResolution(12);  // 12-bit resolution (0-4095)
    analogSetAttenuation(ADC_11db);  // For 3.3V reference, allows 0-3.3V input
    analogSetPinAttenuation(MIC_PIN, ADC_11db);
    
    // Optional: Enable microphone power pin
    if (MIC_VCC_PIN > 0) {
        pinMode(MIC_VCC_PIN, OUTPUT);
        digitalWrite(MIC_VCC_PIN, HIGH);  // Provide 3.3V to microphone
        Serial.println("Microphone power enabled on GPIO33");
    }
    
    Serial.println("Capacitor microphone configured:");
    Serial.println("- GPIO34 (ADC1_CH6) for audio input");
    Serial.println("- 12-bit resolution (0-4095)");
    Serial.println("- 11dB attenuation (0-3.3V range)");
    Serial.println("- 1kHz sampling rate (1ms intervals)");
}

void read_analog_samples() {
    static unsigned long last_sample_time = 0;
    static int16_t dc_offset = 2048;  // Track DC offset for capacitor mic
    static int sample_count = 0;
    
    unsigned long sample_interval = 1000000 / SAMPLE_RATE;  // microseconds between samples
    
    if (micros() - last_sample_time >= sample_interval) {
        int analog_value = analogRead(MIC_PIN);
        
        // Simple DC offset removal for capacitor microphone
        if (sample_count < 1000) {
            // Learn DC offset during first 1000 samples
            dc_offset = (dc_offset * 9 + analog_value) / 10;  // Simple moving average
            sample_count++;
        }
        
        // Remove DC offset and convert to signed 16-bit
        int16_t sample = (analog_value - dc_offset) * 4;  // Moderate scaling
        
        // Add sample to audio processor
        audio_processor.add_sample(sample);
        last_sample_time = micros();
    }
}

void process_audio_frame() {
    if (millis() - last_classification_time > CLASSIFICATION_INTERVAL) {
        AudioFeatures features;
        
        if (audio_processor.extract_features(features)) {
            // Classify the features
            float confidence;
            String classification = classifier.classify(features, confidence);
            
            // Update global variables for serial communication
            last_features = features;
            last_classification = classification;
            last_confidence = confidence;
            has_new_features = true;

            // Send results via serial
            serial_protocol.send_classification_result(features, classification, confidence);

            last_classification_time = millis();
        }
    }
}
