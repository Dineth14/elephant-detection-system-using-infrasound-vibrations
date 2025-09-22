# 🎯 HOW TO RUN - Elephant Detection System

**Complete step-by-step guide for running the ESP32 Elephant Detection System**

---

## 🚀 Quick Start (Recommended)

### 🎯 **One-Click Launch:**
```bash
start_elephant_system.bat
```

**This single command will:**
- ✅ Check and install Python if needed
- ✅ Create virtual environment automatically  
- ✅ Install all Python dependencies
- ✅ Build ESP32 firmware with PlatformIO
- ✅ Upload firmware to ESP32
- ✅ Launch GUI interface
- ✅ Establish USB communication

**Time Required:** 2-5 minutes (first run), 30 seconds (subsequent runs)

---

## 📋 Prerequisites

### 🔌 **Hardware Setup:**
1. **ESP32 Board** - Any ESP32 development board
2. **Microphone** - Analog microphone connected to **GPIO34**
3. **USB Cable** - Connect ESP32 to computer
4. **Computer** - Windows, Linux, or Mac with USB port

### 💻 **Software Requirements:**
- **Python 3.7 or higher** (will be installed automatically if missing)
- **Internet connection** (for initial setup only)
- **USB drivers** (usually automatic on Windows 10+)

---

## 🔧 Detailed Setup Instructions

### **Step 1: Download and Prepare**
1. Download/clone the project to your computer
2. Navigate to the project folder
3. Ensure ESP32 is connected via USB

### **Step 2: Run the System**
**Option A - Automatic Setup (Recommended):**
```bash
# Double-click or run:
start_elephant_system.bat
```

**Option B - Manual Setup:**
```bash
# If automatic setup fails, try manual steps:
python -m pip install -r requirements.txt
python python_gui/noise_logger_gui.py
```

### **Step 3: First-Time Setup**
The first run will:
1. **Install PlatformIO** (ESP32 build system)
2. **Download ESP32 packages** (~100MB)
3. **Build firmware** (2-3 minutes)
4. **Upload to ESP32** (30 seconds)
5. **Launch GUI** automatically

---

## 🖥️ GUI Operation

### 🎮 **Main Interface:**
- **Connection Status** - Shows ESP32 communication status
- **Real-time Features** - 8 audio features updating live
- **Feature Values** - Numerical display of all audio characteristics
- **System Information** - Performance metrics and status

### 📊 **Understanding the Features:**
1. **RMS** - Overall audio energy level
2. **Infrasound** - Elephant frequency range (5-35Hz) 
3. **Low Band** - Mid-range elephant sounds (35-80Hz)
4. **Mid Band** - Higher elephant frequencies (80-250Hz)
5. **Spectral Centroid** - Center frequency of audio spectrum
6. **Spectral Flux** - Rate of spectral change
7. **Temporal Envelope** - Peak amplitude detection
8. **Dominant Frequency** - Main frequency component

### 🎤 **Data Collection:**
- **Record Samples** - Use GUI to capture audio snippets
- **Label Data** - Classify as "elephant" or "background"
- **Export Data** - Save feature sets for training
- **Monitor Live** - Watch real-time classification results

---

## 🔍 Troubleshooting

### ❌ **ESP32 Not Detected:**
```bash
# Check COM port:
python -m serial.tools.list_ports

# Manual ESP32 test:
python test_esp32_direct.py

# Reset ESP32:
# Press RESET button on ESP32 board
```

### ❌ **Python Issues:**
```bash
# Check Python installation:
python --version

# Install requirements manually:
pip install pyserial tkinter numpy matplotlib

# Run GUI directly:
python python_gui/noise_logger_gui.py
```

### ❌ **Build Errors:**
```bash
# Clean build:
cd esp32_firmware
pio run --target clean
pio run --target upload

# Check PlatformIO:
pip install platformio
pio update
```

### ❌ **No Audio Features:**
1. **Check microphone connection** to GPIO34
2. **Verify ESP32 power** (LED should be on)
3. **Test with hand clap** (should see feature changes)
4. **Reset ESP32** and restart GUI

---

## 🎯 Launch Options

### 🚀 **Main Launchers:**
- **`start_elephant_system.bat`** - Complete system setup and launch
- **`run_gui.bat`** - GUI only (if ESP32 already programmed)

### 🧪 **Testing & Validation:**
- **`test_esp32_direct.py`** - Direct ESP32 communication test
- **`test_all_features.py`** - Validate all 8 audio features
- **`diagnose_esp32.py`** - Hardware diagnostic tool

### 🔧 **Manual Operations:**
```bash
# Build ESP32 firmware only:
cd esp32_firmware
pio run

# Upload firmware only:
cd esp32_firmware  
pio run --target upload

# Run GUI only:
python python_gui/noise_logger_gui.py

# Test features only:
python test_all_features.py
```

---

## 📈 Expected Performance

### ✅ **Normal Operation:**
- **Feature Update Rate:** ~1.2 Hz (every 0.8 seconds)
- **USB Communication:** 115200 baud, stable connection
- **Feature Ranges:**
  - Infrasound: 0.9-1.1 (excellent for elephants)
  - Low Band: 0.01-0.12 (good sensitivity)
  - Mid Band: 0.002-0.007 (adequate)
  - Spectral Centroid: 75-95 Hz (perfect range)

### 🎯 **Performance Indicators:**
- **Connection:** Should show "Connected" status in GUI
- **Features:** All 8 values should update regularly
- **Audio Response:** Features should change when making noise
- **Stability:** System should run for hours without issues

---

## 🎤 Audio Testing

### 🔊 **Quick Tests:**
1. **Hand Clap Test** - Should see immediate feature changes
2. **Voice Test** - Speak near microphone, watch features
3. **Silence Test** - Quiet environment should show low values
4. **Elephant Sound Test** - Play elephant audio, observe patterns

### 📊 **Feature Validation:**
```bash
# Run comprehensive feature test:
python test_all_features.py

# Expected output:
# ✅ All 8 features responding correctly
# ✅ Infrasound optimized for elephants  
# ✅ Real-time updates working
# ✅ USB communication stable
```

---

## 🚨 Emergency Procedures

### 🔄 **Complete Reset:**
1. **Disconnect ESP32** from USB
2. **Close all applications** (GUI, terminals)
3. **Reconnect ESP32** to USB
4. **Run:** `start_elephant_system.bat`

### 🆘 **Recovery Mode:**
```bash
# If system completely fails:
1. Hold BOOT button on ESP32
2. Press RESET button while holding BOOT
3. Release RESET, then release BOOT
4. Run: start_elephant_system.bat
```

### 📞 **Getting Help:**
1. **Check this guide** for common solutions
2. **Run diagnostic tools** to identify issues
3. **Check hardware connections** (USB, microphone)
4. **Review system logs** in terminal output

---

## ✅ Success Checklist

**Your system is working correctly when you see:**

- [ ] ESP32 connects automatically via USB
- [ ] GUI launches and shows "Connected" status  
- [ ] All 8 audio features display numerical values
- [ ] Features update every ~0.8 seconds
- [ ] Making noise changes feature values
- [ ] Infrasound energy responds to low-frequency sounds
- [ ] System runs stably for extended periods

**🎉 Ready for elephant detection!**

---

## 🐘 Next Steps

Once your system is running:

1. **🎯 Field Deployment** - Set up microphone in elephant habitat
2. **📊 Data Collection** - Record elephant and background audio samples  
3. **🤖 Training** - Use collected data to train classification model
4. **📡 Monitoring** - Deploy for real-time elephant detection
5. **🌿 Conservation** - Use system for wildlife protection

**Your advanced elephant detection system is now operational!** 🚀
