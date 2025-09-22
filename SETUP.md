# 🛠️ ESP32 Elephant Detection System - Complete Setup Guide

**Comprehensive setup instructions for hardware and software configuration**

---

## 📖 Table of Contents
- [🎯 Overview](#-overview)
- [📋 Prerequisites](#-prerequisites)
- [🔧 Hardware Setup](#-hardware-setup)
- [💻 Software Installation](#-software-installation)
- [📱 ESP32 Firmware Setup](#-esp32-firmware-setup)
- [🖥️ Python Environment Setup](#️-python-environment-setup)
- [🚀 First Run](#-first-run)
- [🧪 System Testing](#-system-testing)
- [🔧 Advanced Configuration](#-advanced-configuration)
- [🐛 Troubleshooting](#-troubleshooting)
- [📊 Performance Optimization](#-performance-optimization)

---

## 🎯 Overview

This setup guide will take you through the complete installation process for the ESP32 Elephant Detection System. The system requires both hardware assembly and software installation across two platforms:

1. **ESP32 Microcontroller**: Real-time audio processing and machine learning
2. **Computer (Windows/Linux/macOS)**: GUI interface and data analysis

**Total Setup Time**: 15-30 minutes for first-time setup

---

## 📋 Prerequisites

### 🔧 **Hardware Requirements**
| Component | Specification | Source | Notes |
|-----------|--------------|--------|-------|
| **ESP32 Board** | Any ESP32 variant | Amazon, SparkFun, Adafruit | ESP32-WROOM, ESP32-DevKitC, etc. |
| **Microphone** | Analog electret/capacitor | Amazon, electronics stores | 3.3V compatible, small form factor |
| **USB Cable** | USB-A to Micro-USB/USB-C | Included with ESP32 | Data cable (not charging-only) |
| **Breadboard** | Half-size or larger | Optional | For prototyping connections |
| **Jumper Wires** | Male-to-male/female | Optional | For connections |

### 💻 **Software Requirements**
| Component | Version | Platform | Auto-Install |
|-----------|---------|----------|-------------|
| **Python** | 3.7 - 3.12 | Windows/Linux/macOS | ❌ Manual |
| **Git** | Latest | Windows/Linux/macOS | ❌ Manual |
| **VS Code** | Latest | All platforms | ⚠️ Recommended |
| **PlatformIO** | Latest | VS Code extension | ✅ Auto |
| **Python Packages** | See requirements.txt | All platforms | ✅ Auto |

### 🌐 **Network Requirements**
- **Internet connection** (for initial setup and package downloads)
- **GitHub access** (for downloading the repository)

---

## 🔧 Hardware Setup

### 📡 **Step 1: Microphone Connection**

#### 🎤 **Basic Wiring (Electret Microphone)**
```
ESP32 Pin    →    Microphone Pin
─────────────────────────────────
GPIO 34      →    Signal/Output
3.3V         →    VCC/Power  
GND          →    GND/Ground
```

#### 🔌 **Detailed Connection Diagram**
```
ESP32 Development Board
┌─────────────────────┐
│                     │
│  [3.3V] ●───────────┼──● VCC (Red wire)
│                     │
│  [GPIO34] ●─────────┼──● Signal (White/Yellow wire)  
│                     │     
│  [GND] ●────────────┼──● GND (Black wire)
│                     │
└─────────────────────┘
            ▲
            │
    ┌───────────────┐
    │   Microphone  │
    │               │
    │  [●] VCC      │
    │  [●] Signal   │  
    │  [●] GND      │
    └───────────────┘
```

### ⚡ **Step 2: Power and USB Connection**

1. **Connect USB cable** to ESP32 and computer
2. **Verify power LED** on ESP32 turns on
3. **Check device recognition** (Windows Device Manager, Linux `lsusb`, macOS System Report)

### 🧪 **Step 3: Hardware Verification**

#### **Quick Test Circuit**
```bash
# 1. Connect microphone as shown above
# 2. Connect USB to computer
# 3. Open Arduino IDE or PlatformIO Serial Monitor
# 4. Check for ESP32 recognition
```

#### **Expected Behavior**
- ✅ ESP32 powers on (LED indicator)
- ✅ Computer recognizes ESP32 USB device
- ✅ No loose connections or short circuits
- ✅ Microphone securely connected to GPIO34

---

## 💻 Software Installation

### 🐍 **Step 1: Python Installation**

#### **Windows**
```powershell
# Method 1: Download from python.org
# 1. Visit https://python.org/downloads/
# 2. Download Python 3.9+ installer
# 3. Run installer with "Add to PATH" checked
# 4. Verify installation:
python --version
pip --version

# Method 2: Using winget (Windows 10/11)
winget install Python.Python.3.12
```

#### **Linux (Ubuntu/Debian)**
```bash
# Update package manager
sudo apt update

# Install Python and pip
sudo apt install python3 python3-pip python3-venv

# Verify installation
python3 --version
pip3 --version
```

#### **macOS**
```bash
# Method 1: Using Homebrew (recommended)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install python

# Method 2: Download from python.org
# Visit https://python.org/downloads/macos/

# Verify installation
python3 --version
pip3 --version
```

### 📁 **Step 2: Download Project**

#### **Method 1: Git Clone (Recommended)**
```bash
# Clone the repository
git clone https://github.com/yourusername/elephant-detection-system-using-infrasound-vibrations.git

# Navigate to project directory
cd elephant-detection-system-using-infrasound-vibrations
```

#### **Method 2: Direct Download**
```bash
# 1. Visit GitHub repository page
# 2. Click "Code" → "Download ZIP"
# 3. Extract to desired location
# 4. Open command prompt/terminal in extracted folder
```

### 🔧 **Step 3: VS Code Setup (Recommended)**

#### **Install VS Code**
```bash
# Windows: Download from https://code.visualstudio.com/
# Linux: 
sudo snap install code --classic
# macOS: Download from website or use Homebrew
brew install --cask visual-studio-code
```

#### **Install PlatformIO Extension**
```bash
# 1. Open VS Code
# 2. Go to Extensions (Ctrl+Shift+X)
# 3. Search "PlatformIO IDE"
# 4. Install by PlatformIO
# 5. Reload VS Code when prompted
```

---

## 📱 ESP32 Firmware Setup

### 🔧 **Method 1: Automated Setup (Recommended)**
```bash
# Run the batch file (Windows)
run_advanced.bat
# OR run_simple.bat

# This will automatically:
# - Install PlatformIO if needed
# - Build ESP32 firmware
# - Upload to connected ESP32
# - Launch GUI
```

### 🔨 **Method 2: Manual Build (Advanced)**

#### **Step 1: Install PlatformIO Core**
```bash
# Install PlatformIO Core
pip install platformio

# Verify installation
pio --version
```

#### **Step 2: Build and Upload Firmware**
```bash
# Navigate to firmware directory
cd esp32_firmware

# Install project dependencies
pio pkg install

# Build firmware
pio run

# Upload to ESP32 (connect ESP32 first)
pio run --target upload

# Monitor serial output (optional)
pio device monitor
```

### 📋 **Firmware Configuration Options**

#### **platformio.ini Configuration**
```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200

# Custom build options
build_flags = 
    -DSAMPLE_RATE=1000
    -DFEATURE_COUNT=8
    -DSERIAL_BAUD=115200

# Libraries (auto-installed)
lib_deps = 
    arduinoFFT@^2.0.0
    ArduinoJson@^7.0.0
```

#### **Hardware Configuration (main.cpp)**
```cpp
// Pin definitions (customizable)
#define MIC_PIN 34         // Microphone input pin
#define MIC_VCC_PIN 33     // Optional: Microphone power pin

// Audio configuration
#define SAMPLE_RATE 1000   // 1 kHz sampling
#define BUFFER_SIZE 256    // 256-sample frames
```

---

## 🖥️ Python Environment Setup

### 📦 **Step 1: Install Dependencies**

#### **Automatic Installation (Recommended)**
```bash
# The batch files handle this automatically:
run_advanced.bat    # Windows
run_simple.bat      # Windows

# Or use Python launchers:
python launch_advanced_gui.py
python launch_gui.py
```

#### **Manual Installation**
```bash
# Install all required packages
pip install -r requirements.txt

# Individual package installation
pip install pyserial numpy matplotlib pandas tkinter
```

### 🔍 **Step 2: Verify Python Environment**
```python
# Test script: test_python_environment.py
import sys
print(f"Python version: {sys.version}")

try:
    import serial
    print("✅ PySerial installed")
except ImportError:
    print("❌ PySerial missing")

try:
    import numpy
    print("✅ NumPy installed")
except ImportError:
    print("❌ NumPy missing")

try:
    import matplotlib
    print("✅ Matplotlib installed")
except ImportError:
    print("❌ Matplotlib missing")

try:
    import tkinter
    print("✅ Tkinter available")
except ImportError:
    print("❌ Tkinter missing")
```

### 🌐 **Step 3: Virtual Environment (Optional but Recommended)**
```bash
# Create virtual environment
python -m venv elephant_detection_env

# Activate virtual environment
# Windows:
elephant_detection_env\Scripts\activate
# Linux/macOS:
source elephant_detection_env/bin/activate

# Install packages in virtual environment
pip install -r requirements.txt

# Deactivate when done
deactivate
```

---

## 🚀 First Run

### 🎯 **Complete System Launch**

#### **Option 1: One-Click Launch**
```bash
# Windows - Double-click one of these:
run_advanced.bat     # Full-featured GUI
run_simple.bat       # Clean, simple GUI

# The batch files will:
# ✅ Check Python installation
# ✅ Install missing packages
# ✅ Build and upload ESP32 firmware
# ✅ Launch GUI interface
# ✅ Auto-connect to ESP32
```

#### **Option 2: Step-by-Step Launch**
```bash
# 1. Upload ESP32 firmware
cd esp32_firmware
pio run --target upload

# 2. Launch Python GUI
cd ..
python launch_advanced_gui.py
# OR
python python_gui/simple_elephant_gui.py

# 3. Connect ESP32 in GUI
# Click "Connect" button or wait for auto-connection
```

### 🔍 **Expected First Run Behavior**

#### **ESP32 Firmware**
```
ESP32 Elephant Logger Starting (USB-Only Mode)...
🔌 USB connectivity enabled, Bluetooth disabled
AudioProcessor initialized: 8 features, 1000 Hz
KNN Classifier ready: k=5, features=8
Serial protocol active: 115200 baud
System ready for audio processing...
```

#### **Python GUI**
```
🚀 Advanced Elephant Detection System Ready
🔍 Searching for ESP32 device...
✅ Found ESP32 on COM3 (or /dev/ttyUSB0)
✅ Connected to ESP32 successfully
📊 Receiving feature data...
```

---

## 🧪 System Testing

### 🧩 **Step 1: Built-in System Tests**
```bash
# Run comprehensive system validation
python test_all_fixes.py

# Expected output:
🧪 Testing Elephant Detection System Fixes
==================================================
1. Testing Classification Parsing: ✅ PASSED
2. Testing Confidence Threshold: ✅ PASSED  
3. Testing 5-Second Timer Logic: ✅ PASSED
🎉 ALL TESTS PASSED!
```

### 🎮 **Step 2: GUI Testing**

#### **Test Detection Visual**
1. **Launch GUI**: Use batch file or Python command
2. **Connect ESP32**: Should auto-connect or click "Connect"
3. **Click TEST button**: Located in Quick Controls section
4. **Verify Display**: 
   - Red "🐘 ELEPHANT DETECTED! 🚨" panel appears
   - 5-second countdown timer: "Detection active: 5.0s remaining"
   - System bell sound (if audio enabled)
   - Debug messages in status log

#### **Test Real Audio Processing**
1. **Make noise near microphone**: Clap hands, speak, play music
2. **Watch feature updates**: Values should change in real-time
3. **Monitor classification**: Check for "elephant" or "no_elephant" results
4. **Verify serial data**: Look for incoming ESP32 messages in status log

### 📊 **Step 3: Performance Validation**

#### **Feature Update Rate Test**
```bash
# Expected performance metrics:
- Audio sampling: 1000 Hz continuous
- Feature extraction: ~3.9 Hz (every 256ms)  
- GUI updates: 1.2 Hz (controlled transmission)
- Serial communication: 115200 baud, stable
- Memory usage: ~25KB RAM on ESP32
```

#### **Connection Stability Test**
```bash
# Run for extended period (5-10 minutes)
# Check for:
✅ No connection drops
✅ Consistent data reception
✅ No memory leaks
✅ Stable feature values
✅ Responsive GUI
```

---

## 🔧 Advanced Configuration

### ⚙️ **ESP32 Firmware Customization**

#### **Audio Processing Parameters**
```cpp
// In main.cpp or AudioProcessor configuration
#define SAMPLE_RATE 1000        // Sampling frequency (Hz)
#define BUFFER_SIZE 256         // Frame size (samples)
#define FFT_SIZE 128           // FFT resolution
#define LOW_PASS_FREQ 200      // Anti-aliasing filter (Hz)

// Feature extraction bands
#define INFRASOUND_LOW 5       // Infrasound lower bound (Hz)  
#define INFRASOUND_HIGH 35     // Infrasound upper bound (Hz)
#define LOW_BAND_HIGH 80       // Low band upper bound (Hz)
#define MID_BAND_HIGH 250      // Mid band upper bound (Hz)
```

#### **Machine Learning Parameters**
```cpp
// In KNNClassifier configuration
#define K_NEIGHBORS 5          // k-NN parameter
#define MIN_CONFIDENCE 0.5     // Minimum detection confidence
#define MAX_TRAINING_SAMPLES 100  // Training data limit
```

### 🖥️ **Python GUI Customization**

#### **Detection Thresholds**
```python
# In simple_elephant_gui.py or advanced_elephant_gui.py
class ElephantGUI:
    def __init__(self):
        # Detection parameters
        self.high_confidence_threshold = 0.5    # High confidence detection
        self.medium_confidence_threshold = 0.3  # Medium confidence detection  
        self.detection_timer_duration = 5.0     # Persistence time (seconds)
        
        # GUI update rates
        self.data_queue_interval = 50          # Data processing (ms)
        self.plot_update_interval = 100        # Plot refresh (ms)
```

#### **Serial Communication**
```python
# Serial port configuration
SERIAL_BAUD_RATE = 115200     # Must match ESP32 setting
SERIAL_TIMEOUT = 1.0          # Read timeout (seconds)
AUTO_RECONNECT = True         # Automatic reconnection
```

### 📊 **Data Logging and Export**

#### **Enable Data Recording**
```python
# In GUI, enable data logging:
self.enable_data_logging = True
self.log_file_path = "elephant_detection_data.csv"
self.log_features = True
self.log_classifications = True
```

#### **Export Formats**
- **CSV**: Feature data and timestamps
- **JSON**: Complete session data with metadata  
- **Audio**: WAV file export (if raw audio saved)
- **Training Data**: Labeled samples for ML training

---

## 🐛 Troubleshooting

### 🔌 **Hardware Issues**

#### **ESP32 Not Detected**
```bash
# Problem: Computer doesn't recognize ESP32
# Solutions:
1. Check USB cable (must be data cable, not charge-only)
2. Install ESP32 drivers:
   # Windows: Download CP210x or CH340 drivers
   # Linux: Usually automatic, check with `lsusb`
   # macOS: Install drivers from Silicon Labs or WCH

3. Try different USB port
4. Press ESP32 reset button
5. Check Device Manager (Windows) for unknown devices
```

#### **Microphone Connection Issues**
```bash
# Problem: No audio input or poor signal quality
# Solutions:
1. Verify wiring: GPIO34 (signal), 3.3V (power), GND (ground)
2. Check microphone type: Must be analog output
3. Test microphone with multimeter (should show voltage variation)
4. Try different microphone
5. Check for loose connections
```

### 💻 **Software Issues**

#### **Python Installation Problems**
```bash
# Problem: Python not found or wrong version
# Solutions:

# Windows:
1. Download Python from python.org (not Microsoft Store version)
2. Ensure "Add to PATH" was checked during installation
3. Restart command prompt after installation
4. Check: python --version (should be 3.7+)

# Linux:
sudo apt update
sudo apt install python3 python3-pip
# Check: python3 --version

# macOS:
brew install python
# Check: python3 --version
```

#### **Package Installation Failures**
```bash
# Problem: pip install fails or packages missing
# Solutions:
1. Update pip: python -m pip install --upgrade pip
2. Use virtual environment to avoid conflicts
3. Install individual packages:
   pip install pyserial
   pip install numpy
   pip install matplotlib
   
4. For matplotlib issues on Linux:
   sudo apt install python3-tk
   
5. For Windows permission issues:
   pip install --user packagename
```

### 🔧 **ESP32 Firmware Issues**

#### **Build/Upload Failures**
```bash
# Problem: PlatformIO build or upload fails
# Solutions:

1. Install/update PlatformIO:
   pip install -U platformio
   
2. Clean build directory:
   pio run --target clean
   pio run
   
3. Check ESP32 connection and try different upload speeds:
   # In platformio.ini:
   upload_speed = 921600   # Try 460800 or 115200 if failing
   
4. Manual ESP32 reset during upload:
   # Hold BOOT button, press RESET, release BOOT when upload starts

5. Check COM port availability:
   pio device list
```

#### **Runtime Errors**
```bash
# Problem: ESP32 crashes, resets, or produces errors
# Solutions:

1. Check serial monitor output:
   pio device monitor
   
2. Verify power supply (stable 5V from USB)
3. Check for memory leaks in code
4. Reduce sample rate if performance issues:
   # Change SAMPLE_RATE from 1000 to 500 Hz
   
5. Factory reset ESP32:
   # Hold BOOT and RESET, release RESET, upload new firmware
```

### 🖥️ **GUI Issues**

#### **Connection Problems**
```bash
# Problem: GUI can't connect to ESP32
# Solutions:

1. Check ESP32 is running (serial monitor shows output)
2. Close other serial applications (Arduino IDE, PuTTY, etc.)
3. Try manual COM port selection
4. Restart ESP32 and GUI application
5. Check firewall/antivirus blocking serial access

# Debug connection:
python -c "import serial.tools.list_ports; print(list(serial.tools.list_ports.comports()))"
```

#### **Performance Issues**
```bash
# Problem: GUI slow, freezing, or high CPU usage
# Solutions:

1. Close other applications using CPU
2. Reduce GUI update frequency:
   # In GUI code, increase update intervals
   
3. Disable real-time plotting in advanced GUI
4. Use simple GUI instead of advanced
5. Check available RAM (GUI needs ~100MB)
```

---

## 📊 Performance Optimization

### ⚡ **ESP32 Optimization**

#### **Memory Management**
```cpp
// Optimize memory usage
#define SAMPLE_BUFFER_SIZE 256    // Keep buffer size reasonable
#define MAX_FEATURES 8            // Don't add unnecessary features
#define FFT_BUFFER_STATIC         // Use static allocation

// Reduce string operations
Serial.print("F:");  // Use short format strings
Serial.println(feature_value, 4);  // Limit decimal places
```

#### **Processing Speed**
```cpp
// Optimize audio processing loop
void loop() {
    // Minimize operations in main loop
    if (audio_ready) {
        process_audio_frame();  // Batch processing
        audio_ready = false;
    }
    
    // Reduce serial transmission frequency
    if (millis() - last_transmission > 833) {  // ~1.2 Hz
        send_features();
        last_transmission = millis();
    }
}
```

### 🖥️ **Python GUI Optimization**

#### **Efficient Data Processing**
```python
# Use efficient data structures
import collections
self.feature_buffer = collections.deque(maxlen=1000)  # Circular buffer

# Batch GUI updates
def update_gui(self):
    # Process all queued data at once
    updates = []
    while not self.data_queue.empty():
        updates.append(self.data_queue.get())
    
    # Single GUI update for all data
    self.process_batch_updates(updates)
```

#### **Plot Performance**
```python
# Optimize matplotlib plots
import matplotlib
matplotlib.use('TkAgg')  # Faster backend for Tkinter

# Limit plot data points
max_plot_points = 500
if len(self.time_data) > max_plot_points:
    self.time_data = self.time_data[-max_plot_points:]
    self.feature_data = self.feature_data[-max_plot_points:]
```

### 📈 **System-wide Optimization**

#### **Recommended Settings**
```bash
# ESP32 Configuration
Sample Rate: 1000 Hz (optimal for infrasound)
Buffer Size: 256 samples (good latency/performance balance)
Transmission Rate: 1.2 Hz (stable GUI performance)
Serial Baud: 115200 (reliable communication)

# Python GUI Configuration  
Update Interval: 50ms (responsive but not overwhelming)
Plot Refresh: 100ms (smooth visualization)
Data Buffer: 1000 samples (reasonable memory usage)
```

---

## 🎉 Setup Complete!

**Congratulations! Your ESP32 Elephant Detection System is now fully configured and ready for use.**

### ✅ **What You Should Have**
- ✅ ESP32 with properly connected microphone
- ✅ Uploaded and running firmware
- ✅ Python environment with all dependencies
- ✅ Functional GUI with real-time detection
- ✅ Working TEST button for system validation
- ✅ Debug logging for troubleshooting

### 🚀 **Next Steps**
1. **Field Deployment**: Set up microphone in elephant habitat
2. **Data Collection**: Record elephant and non-elephant audio samples
3. **Model Training**: Train k-NN classifier with real-world data
4. **Monitoring**: Use system for continuous elephant detection

### 📚 **Additional Resources**
- **README.md**: Comprehensive system documentation
- **GitHub Issues**: Community support and bug reports  
- **Scientific Papers**: Research on elephant infrasound communication
- **Conservation Organizations**: Wildlife monitoring best practices

**Happy elephant monitoring! 🐘🌿**