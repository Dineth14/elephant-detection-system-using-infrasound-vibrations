# 🐘 Simple Elephant Detection System

**Easy-to-use real-time elephant detection with ESP32 and Python GUI**

## 🚀 Quick Start

### Option 1: Simple GUI (Recommended)
```bash
# Windows
run_simple.bat

# Linux/Mac
python run_simple_gui.py
```

### Option 2: Original Advanced GUI
```bash
# Windows
start_elephant_system.bat

# Linux/Mac
python python_gui/noise_logger_gui.py
```

## 📋 What's Fixed

✅ **ESP32 Audio Processing**
- Fixed buffer management for proper feature extraction
- Corrected audio filtering (high-pass + low-pass)
- Improved feature calculation accuracy
- Fixed data transmission format

✅ **Serial Communication**
- Synchronized data format between ESP32 and GUI
- Added proper error handling
- Improved connection reliability
- Auto-detection of ESP32 ports

✅ **Simple GUI Interface**
- Clean, easy-to-use interface
- Real-time feature display
- Automatic ESP32 detection
- Live elephant detection alerts
- Data labeling and saving

✅ **System Integration**
- Fixed all communication issues
- Improved stability and reliability
- Better error handling and logging
- Simplified setup process

## 🔧 Hardware Setup

1. **Connect ESP32 to computer via USB**
2. **Connect microphone to GPIO34 (analog input)**
3. **Ensure ESP32 is powered and recognized**

## 🖥️ Software Requirements

- **Python 3.7+** (automatically checked)
- **pyserial** (automatically installed)
- **tkinter** (comes with Python)

## 📊 Features

### Audio Processing (ESP32)
- **Sampling Rate:** 1kHz
- **Frame Size:** 256 samples (256ms windows)
- **Features:** 8 optimized audio features
  - RMS Energy
  - Infrasound Energy (5-35Hz)
  - Low Band Energy (35-80Hz)
  - Mid Band Energy (80-250Hz)
  - Spectral Centroid
  - Dominant Frequency
  - Temporal Envelope
  - Spectral Flux

### GUI Features
- **Real-time Detection:** Live elephant classification
- **Feature Monitoring:** All 8 audio features displayed
- **Data Labeling:** Label sounds as elephant/not elephant
- **Data Management:** Save and clear training data
- **Connection Status:** Automatic ESP32 detection
- **Logging:** Detailed system logs

## 🎯 Usage

### 1. Start the System
```bash
# Run the simple GUI
run_simple.bat
```

### 2. Connect ESP32
- The GUI will automatically detect your ESP32
- If not detected, click "Connect" to try manually
- Status will show "Connected" when successful

### 3. Monitor Detection
- Watch the detection panel for elephant alerts
- View real-time audio features
- Check the status log for system information

### 4. Label Data
- Click "🐘 Label as Elephant" when you hear elephant sounds
- Click "🚫 Label as Not Elephant" for other sounds
- Use "💾 Save Data" to store labeled samples

### 5. Train the System
- Collect labeled samples over time
- The system will learn to distinguish elephant sounds
- More data = better detection accuracy

## 🔍 Troubleshooting

### ESP32 Not Detected
1. Check USB cable connection
2. Verify ESP32 is powered on
3. Install USB drivers if needed
4. Try different USB port
5. Check Windows Device Manager

### No Audio Features
1. Check microphone connection to GPIO34
2. Verify ESP32 is running the correct firmware
3. Try making noise near the microphone
4. Check the status log for errors

### GUI Issues
1. Make sure Python is installed
2. Check that all dependencies are installed
3. Try running from command line to see error messages
4. Restart the application

## 📁 File Structure

```
📁 Elephant Detection System/
├── 🚀 run_simple.bat              # Simple launcher (Windows)
├── 🐍 run_simple_gui.py           # Simple launcher (Python)
├── 🖼️ python_gui/
│   ├── simple_elephant_gui.py     # Simple GUI (NEW)
│   └── noise_logger_gui.py        # Advanced GUI
├── 🔧 esp32_firmware/
│   ├── src/main.cpp               # Main ESP32 code
│   └── lib/                       # Audio processing libraries
├── 🧪 test_all_features.py        # Feature testing
└── 📖 SIMPLE_SETUP.md             # This file
```

## 🎉 Success Indicators

Your system is working correctly when you see:

- ✅ ESP32 connects automatically
- ✅ GUI shows "Connected" status
- ✅ All 8 audio features display numerical values
- ✅ Features update every ~0.8 seconds
- ✅ Making noise changes feature values
- ✅ Detection panel shows classification results

## 🐘 Next Steps

1. **Field Deployment:** Set up microphone in elephant habitat
2. **Data Collection:** Record elephant and background audio samples
3. **Training:** Use collected data to train the classification model
4. **Monitoring:** Deploy for real-time elephant detection
5. **Conservation:** Use system for wildlife protection

## 📞 Support

If you encounter issues:

1. Check the status log in the GUI
2. Run `test_all_features.py` to validate ESP32 communication
3. Check hardware connections
4. Verify all software requirements are met

**Your elephant detection system is now ready for wildlife conservation!** 🌿
