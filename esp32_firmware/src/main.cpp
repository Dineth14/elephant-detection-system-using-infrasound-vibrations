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
    delay(2000); // Initial delay for power stabilization
    
    Serial.println("ESP32 Elephant Logger Starting (USB-Only Mode)...");
    Serial.println("🔌 USB connectivity enabled, Bluetooth disabled");
    Serial.flush();
    
    // Initialize SPIFFS
    if (!SPIFFS.begin(true)) {
        Serial.println("ERROR:SPIFFS initialization failed");
        return;
    }
    
    // Initialize audio processor with improved feature extraction
    audio_processor.initialize();
    Serial.println("Audio processor initialized (1kHz, 256-sample frames, enhanced frequency detection)");
    
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
    
    Serial.println("ESP32_NOISE_LOGGER_READY");
    
    // Initialize audio input
    init_analog_microphone();
    
    Serial.println("Setup complete - ready for operation (USB-only)");
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
    Serial.println("- Enhanced frequency detection (10-200Hz optimized)");
}

void read_analog_samples() {
    static unsigned long last_sample_time = 0;
    
    // Sample at exactly 1kHz (1ms intervals)
    if (millis() - last_sample_time >= 1) {
        last_sample_time = millis();
        
        // Read ADC value
        int raw_value = analogRead(MIC_PIN);
        
        // Convert to voltage (0-3.3V range with 12-bit ADC)
        float voltage = (raw_value * 3.3) / 4095.0;
        
        // Convert to signed 16-bit for audio processing
        // Center around 0 (assuming 1.65V DC bias)
        int16_t sample = (int16_t)((voltage - 1.65) * 10000);  // Scale for processing
        
        // Add sample to audio processor
        audio_processor.add_sample(sample);
    }
}

void process_audio_frame() {
    static unsigned long last_feature_time = 0;
    const unsigned long FEATURE_INTERVAL = 800;  // Send features every 800ms (1.25 Hz)
    
    AudioFeatures features;
    
    // Extract features if frame is ready
    if (audio_processor.extract_features(features)) {
        // Store features globally
        last_features = features;
        has_new_features = true;
        
        // Rate limit the feature transmission
        if (millis() - last_feature_time >= FEATURE_INTERVAL) {
            // Send features via USB (features only)
            serial_protocol.send_features(features);
            
            // Perform classification
            String classification = classifier.classify(features, last_confidence);
            
            // Ensure we have a valid classification
            if (classification.length() == 0) {
                classification = "not_elephant";  // Fallback
            }
            
            last_classification = classification;
            last_classification_time = millis();
            
            // Send classification result via USB (separate message)
            serial_protocol.send_classification(features, classification, last_confidence);
            
            last_feature_time = millis();
        }
        
        // Reset audio buffer for next frame
        audio_processor.reset_buffer();
    }
}
