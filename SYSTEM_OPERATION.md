
# ESP32 Elephant Acoustic Logger - System Operation

**Author:** Dineth Perera

**License:** MIT License (see LICENSE file)

## System Overview

The ESP32 Elephant Logger is a real-time audio classification system for detecting elephant rumbles and calls. It uses optimized low-frequency digital filtering, extracts elephant-specific features, and classifies sounds as "elephant" or "not_elephant" using a k-NN algorithm. The system is designed for robust field deployment and real-time monitoring with enhanced elephant sensitivity.

## 1. Audio Sample Capture

### Hardware Signal Path
```
Microphone → ESP32 GPIO34 (ADC) → Digital Processing → Classification → Serial Output
```

### Microphone Signal Conditioning
```cpp
// In main.cpp - init_analog_microphone()
analogReadResolution(12);           // 12-bit ADC (0-4095 values)
analogSetAttenuation(ADC_11db);     // 0-3.3V input range
```

**What happens:**
1. **Sound waves** hit the capacitor microphone diaphragm
2. **Capacitance changes** create voltage variations (AC signal)
3. **Bias voltage** (3.3V) powers the electret microphone
4. **AC-coupled signal** goes to ESP32 GPIO34 analog input
5. **12-bit ADC** converts analog voltage to digital values (0-4095)

### Sampling Loop
```cpp
// In main.cpp - read_analog_samples()
void read_analog_samples() {
    static unsigned long last_sample_time = 0;
    unsigned long sample_interval = 1000000 / 1000;  // 1ms for 1kHz
    if (micros() - last_sample_time >= sample_interval) {
        int analog_value = analogRead(MIC_PIN);
        // Process the sample...
        last_sample_time = micros();
    }
}
```

## 2. Sample Storage and Buffering

### Circular Buffer System
```cpp
class AudioProcessor {
private:
    std::vector<int16_t> audio_buffer;  // 256 samples
    int buffer_index;                   // Current write position
};

void AudioProcessor::add_sample(int16_t sample) {
    audio_buffer[buffer_index] = sample;
    buffer_index = (buffer_index + 1) % 256;  // Wrap around at 256
}
```

## 3. Digital Signal Processing

### Single-Stage Optimized Filtering (Enhanced for Elephants)

#### Low-Pass Filter Only (200 Hz cutoff)
```cpp
float AudioProcessor::apply_low_pass_filter(float input) {
    // 1st order low-pass: y[n] = αx[n] + (1-α)y[n-1]
    // α calculated for 200Hz at 1kHz
    // Preserves full elephant range 0-200Hz including true infrasound
    ...existing code...
}
```

**Enhancement Note:** High-pass filter removed to preserve elephant infrasound (0-20Hz) and low-frequency vocalizations critical for accurate detection.

## 4. Feature Extraction Process

### Frame-Based Processing
```cpp
bool AudioProcessor::extract_features(AudioFeatures& features) {
    if (buffer_index != 0) return false;
    std::vector<float> frame(256);
    for (int i = 0; i < 256; i++) {
        frame[i] = audio_buffer[i] / 32768.0;
    }
    apply_hamming_window(frame);
    // Extract features...
}
```

### Features Extracted

1. **RMS (Root Mean Square)**: Overall energy/volume level
2. **Spectral Centroid**: Center of mass of the spectrum (0–500Hz)
3. **Infrasound Energy**: Energy in 10–40Hz band (elephant rumbles)
4. **Low Band Energy**: Energy in 40–100Hz band
5. **Mid Band Energy**: Energy in 100–200Hz band
6. **Dominant Frequency**: Frequency bin with highest energy
7. **Temporal Envelope**: Maximum absolute amplitude in frame
8. **Spectral Flux**: Rate of change in spectral content

## 5. Machine Learning Classification

### k-Nearest Neighbors Algorithm
```cpp
String KNNClassifier::classify(const AudioFeatures& features, float& confidence) {
    // ...existing code...
}
```

### Distance Calculation
```cpp
float KNNClassifier::compute_distance(const AudioFeatures& a, const AudioFeatures& b) {
    float dist = 0;
    dist += pow(a.rms - b.rms, 2);
    dist += pow((a.spectral_centroid - b.spectral_centroid) / 100.0, 2);
    dist += pow(a.infrasound_energy - b.infrasound_energy, 2);
    dist += pow(a.low_band_energy - b.low_band_energy, 2);
    dist += pow(a.mid_band_energy - b.mid_band_energy, 2);
    dist += pow((a.dominant_freq - b.dominant_freq) / 10.0, 2);
    dist += pow(a.temporal_envelope - b.temporal_envelope, 2);
    dist += pow(a.spectral_flux - b.spectral_flux, 2);
    return sqrt(dist);
}
```

## 6. Serial Communication Protocol

### Output Format
```cpp
void SerialProtocol::send_classification_result(const AudioFeatures& features, const String& classification, float confidence) {
    Serial.print("FEATURES:");
    Serial.print(features.rms, 4); Serial.print(",");
    Serial.print(features.spectral_centroid, 1); Serial.print(",");
    Serial.print(features.infrasound_energy, 4); Serial.print(",");
    Serial.print(features.low_band_energy, 4); Serial.print(",");
    Serial.print(features.mid_band_energy, 4); Serial.print(",");
    Serial.print(features.dominant_freq, 1); Serial.print(",");
    Serial.print(features.temporal_envelope, 4); Serial.print(",");
    Serial.print(features.spectral_flux, 4); Serial.print(",");
    Serial.print(classification); Serial.print(",");
    Serial.println(confidence, 3);
}
```

### Command Processing
```cpp
// ...existing code for command handling...
```

## 7. Python GUI Integration

### Data Reception
```python
def process_serial_data(self, line: str) -> None:
    if line.startswith("FEATURES:"):
        self.parse_features(line)
    # ... handle other message types

def parse_features(self, line: str) -> None:
    data = line.split(":")[1].split(",")
    features = {
        "RMS": float(data[0]),
        "Spectral Centroid": float(data[1]),
        "Infrasound Energy": float(data[2]),
        "Low Band Energy": float(data[3]),
        "Mid Band Energy": float(data[4]),
        "Dominant Frequency": float(data[5]),
        "Temporal Envelope": float(data[6]),
        "Spectral Flux": float(data[7]),
    }
    classification = data[8]
    confidence = float(data[9])
    self.update_displays(features, classification, confidence)
```

## 8. System States and Flow Control

### State Machine
```
STARTUP → INITIALIZATION → SAMPLING → PROCESSING → CLASSIFICATION → OUTPUT → [loop back to SAMPLING]
```

### Error Handling
- **Buffer overflow**: Impossible due to circular buffer design
- **ADC failure**: Timeout detection and recovery
- **Memory exhaustion**: Graceful degradation, oldest training data removed
- **Serial errors**: Continue operation, log errors

### Timing Guarantees
- **Hard real-time**: Sample acquisition (must not miss 1kHz timing)
- **Soft real-time**: Feature processing (can tolerate occasional delays)
- **Background**: Serial communication, file I/O

This system provides robust, real-time elephant sound detection on a low-cost microcontroller platform, suitable for field deployment and conservation research.
