# 🐘 ESP32 Elephant Detection System

**Author:** Dineth Perera  
**License:** MIT License (see LICENSE file)

---

## 🚀 Quick Start

### Option 1: Fully Automated (Recommended) ⚡
1. **Double-click `auto_run.bat`**
   - Automatically uploads ESP32 firmware via PlatformIO
   - Launches GUI application
   - Complete system ready in ~15 seconds

### Option 2: Manual Steps
1. **Setup**: Double-click `setup.bat`
   - Creates Python virtual environment
   - Installs all required dependencies
2. **Run**: Double-click `run_gui.bat`
   - Launches the GUI application (firmware upload required separately)
```bash
# Manual setup if needed
# Create virtual environment
python -m venv .venv

# Activate environment (Windows)
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run GUI (firmware must be uploaded separately)
python python_gui/noise_logger_gui.py
```

---

## � System Components

### Core Files
- **`auto_run.bat`** - Complete automated system (firmware + GUI) ⚡
- **`setup.bat`** - One-time environment setup
- **`run_gui.bat`** - GUI launcher only
- **`system_test.py`** - System validation
- **`simulate_esp32.py`** - Hardware simulation for testing

### Testing Without Hardware
```bash
# Test the system (use virtual environment)
.venv\Scripts\python.exe system_test.py

# Run with simulated ESP32 data
.venv\Scripts\python.exe simulate_esp32.py

# Or use global Python (after manual pip install)
python system_test.py
```

---

## 🔧 ESP32 Hardware Setup

### Automated Firmware Upload (Recommended)
1. **Connect ESP32 via USB**
2. **Double-click `auto_run.bat`**
   - Automatically compiles and uploads firmware
   - Launches GUI when ready
   - Shows upload progress and completion

### Manual Firmware Upload
1. Open `esp32_firmware` folder in VS Code with PlatformIO
2. Connect ESP32 via USB
3. Upload firmware using PlatformIO: `pio run --target upload`
4. Run GUI separately with `run_gui.bat`

### Hardware Connections
- **Microphone**: GPIO34 (analog input)
- **Power**: GPIO33 (optional microphone power)
- **Ground**: GND
- **USB**: For serial communication

---

## �️ GUI Features

### Main Interface
- **Connection Panel**: ESP32 serial connection
- **Live Detection**: Real-time elephant classification
- **Audio Features**: 8-dimensional feature display
- **Detection Log**: History of classifications

### Data Management
- **Labeling**: Train the system with "elephant"/"not_elephant" labels
- **Storage**: Data saved to ESP32 flash memory
- **Export**: Retrieve training data via serial
- **Enhanced Features**: Now includes true infrasound (0-20Hz) for better accuracy

---

## 📊 System Verification

Run the test suite to verify everything works:
```bash
python system_test.py
```

Expected output:
```
ESP32 Elephant Detection System - System Test
==================================================
Testing imports...
  [OK] tkinter
  [OK] matplotlib
  [OK] pyserial
  [OK] GUI module

Testing GUI creation...
  [OK] GUI object created successfully

[RESULT] SUCCESS - All tests passed!
```

---

## � Troubleshooting

### Common Issues

**"Python not recognized"**
- Install Python from [python.org](https://python.org)
- Make sure "Add to PATH" is checked during installation

**Virtual environment errors**
- Delete `.venv` folder and run `setup.bat` again

**Import errors**
- Run `setup.bat` to reinstall packages
- Use the virtual environment: `.venv\Scripts\python.exe`

**ESP32 not detected**
- Check USB cable and drivers
- Use Windows Device Manager to find COM port
- Test with `python test_esp32_direct.py`
- **Try automated system**: `auto_run.bat` handles firmware upload automatically

**Automated upload fails**
- Check ESP32 is properly connected to USB
- Ensure PlatformIO is installed (auto_run.bat will attempt installation)
- Use manual upload method if needed

### Validation Commands
```bash
# Test system components (use virtual environment)
.venv\Scripts\python.exe system_test.py

# Test ESP32 communication (hardware required)
.venv\Scripts\python.exe test_esp32_direct.py

# Test without hardware
.venv\Scripts\python.exe simulate_esp32.py
```

---

## 📁 Project Structure

```
ESP32-Elephant-Detection/
├── auto_run.bat             # Complete automated system ⚡
├── setup.bat                # Environment setup
├── run_gui.bat              # GUI launcher only
├── system_test.py           # System test
├── simulate_esp32.py        # Hardware simulation
├── test_esp32_direct.py     # Hardware test
├── requirements.txt         # Dependencies
├── python_gui/              # GUI source code
│   ├── noise_logger_gui.py  # Main GUI application
│   └── retrieve_esp32_dataset.py
└── esp32_firmware/          # ESP32 firmware (Enhanced)
    ├── platformio.ini       # Build configuration
    ├── src/main.cpp         # Main firmware
    └── lib/                 # Audio processing libraries
        ├── AudioProcessor/  # Enhanced: No high-pass filter
        ├── KNNClassifier/   # Machine learning
        └── SerialProtocol/  # Communication
```

---

## ✅ Success Indicators

When everything is working correctly:

1. **Automated Run**: `auto_run.bat` completes firmware upload (shows "SUCCESS" and upload time)
2. **Setup**: `setup.bat` completes without errors
3. **Test**: `system_test.py` shows "SUCCESS - All tests passed!"
4. **GUI**: Window opens with elephant detection interface
5. **Enhanced Audio**: System now preserves 0-200Hz range for better elephant detection
6. **Real-time Updates**: Connect to COM10 in GUI to see live audio features

---

## 🎉 Ready to Use!

Your Enhanced ESP32 Elephant Detection System is now ready for:
- **One-click deployment** with `auto_run.bat`
- **Improved elephant detection** with full infrasound preservation (0-200Hz)
- **Software testing** with simulated data
- **Hardware testing** with real ESP32 and microphone  
- **Field deployment** for enhanced elephant monitoring

### Key Improvements ✨
- **Automated firmware upload**: No manual PlatformIO required
- **Enhanced audio processing**: Preserves critical elephant infrasound (0-80Hz)
- **Better detection accuracy**: Full frequency range optimization
- **Streamlined workflow**: Double-click to deploy and run
