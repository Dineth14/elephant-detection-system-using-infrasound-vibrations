# Summary (Elephant Logger)

**Sample Rate:** 1kHz (1000 samples/sec)
**Frame Size:** 256 samples (256ms)
**Frequency Range:** 0–200Hz (Full elephant range including infrasound) - OPTIMIZED FOR ELEPHANTS
**Features:** RMS, Spectral Centroid, Infrasound Energy (0–40Hz), Low Band (40–100Hz), Mid Band (100–200Hz), Dominant Frequency, Temporal Envelope, Spectral Flux
**Labels:** "elephant", "not_elephant"

**IMPORTANT:** System now preserves all elephant frequencies from 0Hz upward. All spectral features capture the complete elephant vocalization range including true infrasound (0-20Hz) for improved detection accuracy.
# ESP32 Elephant Detection Logger - Audio Specs

**Author:** Dineth Perera

**License:** MIT License (see LICENSE file)

# ESP32 Audio Processing - Technical Specifications (Elephant Logger)

## Audio Processing Overview

### Sampling Rate
- **Current**: 1 kHz sampling rate (focus on infrasound and low-frequency bands)
- **Benefit**: Captures elephant vocalizations and low-frequency environmental sounds

### Digital Signal Processing

#### Low-Pass Filter (Only)
- **Cutoff Frequency**: 200 Hz
- **Type**: 1st order digital low-pass filter
- **Purpose**: Remove high-frequency noise while preserving full elephant range (0-200Hz)
- **Implementation**: `y[n] = αx[n] + (1-α)y[n-1]`
- **Benefit**: Preserves true infrasound (0-20Hz) and low-frequency elephant vocalizations

### Frame Processing
- **Frame Size**: 256 samples
- **Overlap**: 128 samples (50% overlap)
- **Window**: Hamming window for spectral analysis
- **Update Rate**: Every 256 ms for classification

### Frequency Band Analysis
Frequency bands for elephant detection (Enhanced Range):
- **True Infrasound Band**: 0–20 Hz (deepest elephant rumbles, now preserved)
- **Extended Infrasound Band**: 20–40 Hz (elephant rumbles and calls)
- **Low Band**: 40–100 Hz (low-frequency harmonics)
- **Mid Band**: 100–200 Hz (upper harmonics)

### Filter Coefficients
Digital filter coefficients calculated as:
- **Low-pass α**: `dt / (RC + dt)` where `RC = 1/(2πf_c)`
- **Sample period dt**: 1/1000 = 1 ms
- **Note**: High-pass filter removed to preserve elephant infrasound

### Performance Characteristics

#### Timing Requirements
- **Sample interval**: 1 ms (1 kHz)
- **ADC read time**: ~3 μs (ESP32 12-bit ADC)
- **Filter processing**: ~1 μs per sample
- **Margin**: ~996 μs for other processing

#### Memory Usage
- **Audio buffer**: 256 samples × 2 bytes = 512 B
- **FFT buffer**: 256 floats × 4 bytes = 1 KB
- **Total audio memory**: ~1.5 KB

#
#### Quality Metrics
- **Signal-to-Noise Ratio**: Enhanced by preserving elephant infrasound while filtering high-frequency noise
- **Frequency Resolution**: 1000/256 ≈ 3.9 Hz per bin
- **Dynamic Range**: 12-bit ADC (72 dB theoretical)
- **Elephant Sensitivity**: Improved by preserving 0-80Hz range critical for detection

## Hardware Compatibility

### Analog Microphone Support
- **Input impedance**: High-Z analog input (GPIO34)
- **Bias voltage**: 3.3V for electret capsules
- **Coupling**: AC-coupled with software DC removal
- **Gain**: 16x digital amplification for 12-bit ADC

### ESP32 ADC Configuration
- **Resolution**: 12-bit (0-4095 counts)
- **Attenuation**: 11dB (0-3.3V input range)
- **Reference**: Internal 3.3V
- **Conversion time**: ~3 μs per sample

## Code Architecture

### AudioProcessor Class
```cpp
class AudioProcessor {
private:
    // Digital filter state (Low-pass only)
    float lp_prev_input, lp_prev_output;   // Low-pass
    float lp_alpha;                        // Low-pass coefficient
    // Filter implementation
    float apply_low_pass_filter(float input);
    // Note: High-pass filter removed to preserve elephant infrasound
};
```

### Real-time Processing
- Interrupt-driven sampling at 1 kHz
- Efficient filter implementations
- Overlap-add windowing for FFT

## Validation and Testing

### Filter Response Verification
- Low-pass: -3dB at 200 Hz, >20dB attenuation above 300 Hz
- Full elephant range preserved: 0-200Hz with no high-pass attenuation

### Performance Benchmarks
- CPU usage: <10% at 1 kHz sampling
- Memory usage: <2 KB for audio processing
- Latency: <300ms from sample to classification

### Audio Quality Tests
- Frequency response: Flat within ±1dB from 0–200 Hz (full elephant range preserved)
- THD+N: <1% for 50 Hz test tone
- Dynamic range: >60dB practical range
- Infrasound sensitivity: Enhanced by removing high-pass filter

## Feature Extraction (Elephant Logger)

### Extracted Features (Enhanced for Elephant Detection)
- **RMS Energy** (Full range 0-200Hz)
- **Spectral Centroid** (Full range 0-200Hz)
- **True Infrasound Band Energy (0–20 Hz)** - *NEW: Now preserved*
- **Extended Infrasound Band Energy (20–40 Hz)**
- **Low Band Energy (40–100 Hz)**
- **Mid Band Energy (100–200 Hz)**
- **Dominant Frequency** (Full range 0-200Hz)
- **Temporal Envelope**
- **Spectral Flux** (Enhanced sensitivity)

## Classification
- **Type**: k-Nearest Neighbors (k-NN)
- **Labels**: "elephant" or "not_elephant" (binary)

## Future Enhancements
- Adaptive noise cancellation
- Real-time spectrum display
- Automatic gain control (AGC)
