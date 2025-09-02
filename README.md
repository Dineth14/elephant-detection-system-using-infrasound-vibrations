
# 🐘 ESP32 Elepha### 🔊 Enhanced Audio Processing
- **Real-time Audio Processing**: 1kHz sampling, 256-sample frames (256ms windows)  
- **Optimized Digital Filtering**: 200Hz low-pass filter only (high-pass removed for elephant sensitivity)
- **Full Elephant Range Preserved**: 0-200Hz frequency range captures complete elephant vocalizations
- **Enhanced Infrasound Detection**: True infrasound (0-20Hz) now fully preserved
- **8D Feature Extraction**: Comprehensive acoustic analysis with improved sensitivity
- **Offline Machine Learning**: k-NN classifier runs entirely on ESP32
- **Live Binary Classification**: Instant "elephant" or "not_elephant" detection with confidenceection System 

**Author:** Dineth Perera  
**License:** MIT License (see LICENSE file)  


This advanced system detects elephant rumbles and calls using sophisticated low-frequency audio analysis, featuring a modern professional GUI and enhanced real-time performance.

## 🎯 Enhanced Key Features

### 🚀 Modern Professional Interface
- **GitHub-Inspired Dark Theme**: Contemporary visual design with professional color scheme
- **3-Column Smart Layout**: Optimized space utilization (2:2:1 ratio)
- **Modern Card-Based Design**: Clean separation of functional areas with subtle shadows
- **Enhanced Typography**: Segoe UI font family for modern appearance
- **Real-time Status Bar**: Performance metrics and system status
- **66 FPS Performance**: Ultra-responsive real-time updates (15ms intervals)

### � Advanced Audio Processing
- **Real-time Audio Processing**: 1kHz sampling, 256-sample frames (256ms windows)
- **Low-Frequency Digital Filtering**: 10Hz high-pass and 200Hz low-pass filters
- **8D Feature Extraction**: Comprehensive acoustic analysis with color-coded visualization
- **Offline Machine Learning**: k-NN classifier runs entirely on ESP32
- **Live Binary Classification**: Instant "elephant" or "not_elephant" detection with confidence

### 📊 Enhanced Feature Display
- **4x2 Grid Layout**: Modern individual cards for each audio feature
- **Color-Coded Features**: Unique accent colors for easy identification
- **Large Value Display**: Enhanced readability with 14pt bold values
- **Real-time Visualization**: Instant updates with smooth transitions

### 🔗 Smart Connectivity
- **Enhanced Auto-Connection**: Advanced ESP32 detection with hardware recognition
- **Professional Port Selection**: Modern dialog with detailed device information
- **Real-time Port Scanning**: Comprehensive hardware identification
- **Connection Status Monitoring**: Live updates in modern status bar

## 🎨 Modern GUI Features

### Visual Enhancements
- **Maximized Window Support**: Auto-starts at 1600x1000 for optimal space usage
- **Scrollable Interface**: Both vertical and horizontal scrolling with mouse wheel
- **Enhanced Hover Effects**: Smooth button transitions with modern styling
- **Professional Status Bar**: Three-section layout with real-time metrics
- **Modern Detection Indicator**: Large, prominent display with gradient effects

### User Experience
- **Intuitive Layout**: Clear information hierarchy with modern design principles
- **Enhanced Responsiveness**: Smooth scaling across different screen sizes
- **Professional Interactions**: Consistent iconography and visual feedback
- **Color-Coded Information**: Easy distinction between different data types

## 🚀 Quick Start

### Automated Deployment (Recommended) ⚡
1. **Connect ESP32 via USB**
2. **Double-click `auto_run.bat`**
   - Automatically uploads optimized firmware
   - Launches enhanced GUI
   - Complete system ready in ~15 seconds

### Manual Setup
1. **Setup Environment**: Run `setup.bat`
2. **Upload Firmware**: Use PlatformIO or automated script
3. **Launch GUI**: Run `run_gui.bat`

### ESP32 Firmware (Enhanced)
- **Audio Capture**: 1kHz sampling from analog microphone (GPIO34)
- **Optimized Digital Filtering**: 200Hz low-pass filter (high-pass removed for elephant sensitivity)
- **DC Offset Removal**: Adaptive learning from first 2000 samples
- **Enhanced Feature Extraction**: RMS, Spectral Centroid, True Infrasound Energy (0–20Hz), Extended Infrasound (20–40Hz), Low Band Energy (40–100Hz), Mid Band Energy (100–200Hz), Dominant Frequency, Temporal Envelope, Spectral Flux
- **Full Range FFT Processing**: 128 frequency bins covering complete 0–500Hz range
- **Classification**: Offline k-NN classifier with incremental learning
- **Storage**: Persistent dataset storage on ESP32 SPIFFS flash
- **Communication**: Serial protocol for real-time GUI interaction

### Python GUI
- **Smart ESP32 Detection**: Hardware-based identification with VID/PID matching
- **Auto-Connection**: Automatic detection of ESP32 boards by device signatures
- **Manual Port Selection**: User-friendly dialog with detailed port information
- **Live Monitoring**: Real-time display of low-frequency features and binary classification
- **Interactive Labeling**: Quick buttons for "elephant" and "not_elephant"
- **Dataset Management**: Save/load/clear training data on ESP32

## Features Extracted (Enhanced for Elephants)

1. **RMS (Root Mean Square)**: Overall energy/volume level (full 0-200Hz range)
2. **Spectral Centroid**: Center of mass of the spectrum (0–500Hz, optimized for elephant range)
3. **True Infrasound Energy**: Energy in 0–20Hz band (deepest elephant rumbles, now preserved)
4. **Extended Infrasound Energy**: Energy in 20–40Hz band (elephant rumbles and calls)
5. **Low Band Energy**: Energy in 40–100Hz band (low-frequency harmonics)
6. **Mid Band Energy**: Energy in 100–200Hz band (upper harmonics)
7. **Dominant Frequency**: Frequency bin with highest energy (full range)
8. **Temporal Envelope**: Maximum absolute amplitude in frame
9. **Spectral Flux**: Rate of change in spectral content (enhanced sensitivity)


### Real-time Classification (Improved Accuracy)

Once you have labeled samples:
- The system will automatically classify incoming audio as "elephant" or "not_elephant"
- Classifications appear in real-time with confidence scores
- Feature plots show the evolution of low-frequency audio characteristics

### Serial Protocol (ESP32 → GUI)
- `FEATURES:rms,centroid,infra,low_band,mid_band,dom_freq,envelope,flux,label,confidence`
- `STATUS:samples,uptime,memory`
- `LABELED:label,total_samples`
- `DATASET:total,elephant,not_elephant`
- `OK:message` - Success confirmation
- `ERROR:message` - Error notification

## 🎉 Enhanced System Ready!

Your optimized ESP32 Elephant Detection System now features:
- **🚀 One-click deployment** with `auto_run.bat`
- **🔊 Enhanced elephant detection** with full infrasound preservation (0-200Hz)
- **⚡ Automated firmware upload** - no manual PlatformIO required
- **🎯 Improved accuracy** with optimized audio processing
- **🎨 Modern professional GUI** with GitHub-inspired design

### Key Improvements ✨
- **True infrasound detection**: 0-20Hz range now fully preserved
- **Enhanced low-frequency sensitivity**: Critical for elephant detection
- **Streamlined deployment**: Double-click to upload and run
- **Optimized signal processing**: Better sensitivity, less noise

**Ready for field deployment with superior elephant detection capabilities!**
