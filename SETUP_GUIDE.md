# Elephant Detection System - Setup Guide

## Overview
This system consists of:
1. **ESP32 Firmware** - Audio processing and classification on the ESP32
2. **Python GUI** - Real-time visualization and control interface
3. **Serial Communication** - USB communication between ESP32 and Python

## Prerequisites

### Software Requirements
- **Python 3.8+** (tested with Python 3.11.9)
- **PlatformIO** (for ESP32 firmware compilation)
- **ESP32 Board** with microphone
- **USB Cable** for connection

### Python Dependencies
The system automatically installs these packages:
- `pyserial` - Serial communication
- `numpy` - Numerical computing
- `matplotlib` - Plotting and visualization
- `pandas` - Data analysis (advanced GUI only)
- `tkinter` - GUI framework (included with Python)

## Quick Start

### Option 1: Simple GUI (Recommended for beginners)
1. **Connect ESP32** via USB
2. **Run the batch file**: Double-click `run_simple.bat`
3. **Wait for auto-detection** - The GUI will automatically find your ESP32
4. **Start using** - The interface will show real-time audio features and detection

### Option 2: Advanced GUI (For advanced users)
1. **Connect ESP32** via USB
2. **Run the batch file**: Double-click `run_advanced.bat`
3. **Wait for auto-detection** - The GUI will automatically find your ESP32
4. **Use advanced features** - Real-time plotting, data analysis, ML training

### Option 3: Manual Python Launch
```bash
# Simple GUI
python launch_gui.py

# Advanced GUI
python launch_advanced_gui.py
```

## ESP32 Firmware Setup

### Prerequisites
- **PlatformIO** installed
- **ESP32 board** (tested with ESP32-WROOM-32)

### Compile and Upload
1. **Open terminal** in the `esp32_firmware` directory
2. **Compile firmware**:
   ```bash
   pio run
   ```
3. **Upload to ESP32**:
   ```bash
   pio run --target upload
   ```
4. **Monitor serial output**:
   ```bash
   pio device monitor
   ```

### Hardware Setup
- **Microphone**: Connect to GPIO34 (ADC1_CH6)
- **Power**: Connect 3.3V to GPIO33 (optional, for powered microphones)
- **Ground**: Connect to GND

## System Operation

### Connection Process
1. **ESP32 starts** and sends "ESP32_NOISE_LOGGER_READY"
2. **Python GUI** auto-detects the ESP32 port
3. **Serial communication** established at 115200 baud
4. **Real-time data** flows from ESP32 to GUI

### Data Flow
1. **Audio samples** captured at 1kHz on ESP32
2. **Features extracted** every 800ms (1.25 Hz)
3. **Classification** performed using KNN algorithm
4. **Results sent** to Python GUI via USB
5. **GUI displays** real-time RMS amplitude plot and detection

### Features Monitored
- **RMS Energy** - Overall audio level
- **Infrasound (5-35Hz)** - Low-frequency elephant calls
- **Low Band (35-80Hz)** - Mid-low frequency content
- **Mid Band (80-250Hz)** - Mid-frequency content
- **Spectral Centroid** - Frequency center of mass
- **Dominant Frequency** - Peak frequency
- **Temporal Envelope** - Audio envelope shape
- **Spectral Flux** - Frequency change rate

## Troubleshooting

### Common Issues

#### 1. ESP32 Not Detected
**Symptoms**: GUI shows "ESP32 not found"
**Solutions**:
- Check USB cable connection
- Verify ESP32 is powered on
- Install COM port drivers (CP210x, CH340, etc.)
- Try different USB port
- Check Device Manager for COM port

#### 2. Connection Failed
**Symptoms**: "Connection failed" error
**Solutions**:
- Close other applications using the COM port
- Restart the GUI
- Check if ESP32 is running the correct firmware
- Verify baud rate (115200)

#### 3. No Audio Data
**Symptoms**: Features show "--" or 0 values
**Solutions**:
- Check microphone connection to GPIO34
- Verify microphone is working
- Check audio levels (may be too quiet)
- Ensure ESP32 is running the correct firmware

#### 4. GUI Won't Start
**Symptoms**: Python errors when starting
**Solutions**:
- Install required packages: `pip install -r requirements.txt`
- Check Python version (3.8+ required)
- Verify all files are present

### Debug Mode
To see detailed debug information:
1. **Open terminal** in project directory
2. **Run with debug**: `python launch_gui.py`
3. **Check console output** for error messages

## File Structure
```
Ali-Rita--elephant-detection-system-/
├── esp32_firmware/           # ESP32 firmware code
│   ├── src/main.cpp         # Main firmware
│   ├── lib/                 # Custom libraries
│   └── platformio.ini       # Build configuration
├── python_gui/              # Python GUI code
│   ├── simple_elephant_gui.py    # Simple interface
│   └── advanced_elephant_gui.py  # Advanced interface
├── launch_gui.py            # Simple GUI launcher
├── launch_advanced_gui.py   # Advanced GUI launcher
├── run_simple.bat           # Windows batch file (simple)
├── run_advanced.bat         # Windows batch file (advanced)
├── requirements.txt         # Python dependencies
└── SETUP_GUIDE.md          # This file
```

## Advanced Features

### Data Labeling
- **5-second labeling** - Click "ELEPHANT" or "NOT ELEPHANT" buttons
- **Real-time collection** - System collects data during labeling
- **Training data** - Stored for machine learning

### Data Analysis
- **Feature visualization** - Real-time plots of audio features
- **Classification analysis** - Performance metrics
- **Data export** - Save data as JSON or CSV

### Machine Learning
- **KNN Classifier** - Built-in classification algorithm
- **Model training** - Train on labeled data
- **Model testing** - Test classification accuracy
- **Model saving** - Save trained models

## Support
If you encounter issues:
1. **Check this guide** for common solutions
2. **Check console output** for error messages
3. **Verify hardware connections**
4. **Test with simple GUI first**

## Version Information
- **Python GUI**: Version 1.0
- **ESP32 Firmware**: Version 1.0
- **Tested with**: Python 3.11.9, ESP32-WROOM-32
- **Last updated**: 2024
