# 🐘 Advanced Elephant Detection System

**Professional-grade real-time elephant detection with AI-powered analysis and machine learning capabilities**

## 🚀 Quick Start

### **Option 1: Advanced GUI (Recommended)**
```bash
# Windows
run_advanced.bat

# Linux/Mac
python launch_advanced_gui.py
```

### **Option 2: Simple GUI**
```bash
# Windows
run_simple.bat

# Linux/Mac
python launch_gui.py
```

## 🎯 **Advanced Features**

### **📊 Real-time Dashboard**
- **Live Detection Panel**: Large visual indicator with confidence scoring
- **Audio Features Display**: 8 real-time audio features in organized cards
- **Real-time Plotting**: Live visualization of feature trends over time
- **Session Statistics**: Track samples, detections, and accuracy
- **Quick Controls**: One-click labeling and data management

### **📈 Data Analysis Tab**
- **Feature Distribution Analysis**: Statistical analysis of audio features
- **Time Series Analysis**: Trend analysis and pattern recognition
- **Classification Analysis**: Performance metrics and confusion matrices
- **Data Export**: Export to JSON, CSV, or other formats
- **Interactive Visualizations**: Zoom, pan, and analyze data

### **🤖 Machine Learning Tab**
- **Model Training**: Train custom classification models
- **Model Testing**: Validate model performance
- **Model Management**: Save and load trained models
- **Dataset Information**: Track training data statistics
- **Training Results**: Monitor training progress and metrics

### **⚙️ Settings Tab**
- **Audio Configuration**: Adjust sampling rates and sensitivity
- **Detection Thresholds**: Customize classification parameters
- **System Preferences**: GUI themes and display options
- **Export Settings**: Configure data export formats

## 🎮 **How to Use the Advanced GUI**

### **1. Dashboard Tab - Main Interface**

#### **Connection Panel**
- **Auto-detection**: Automatically finds and connects to ESP32
- **Manual Connection**: Click "Connect" if auto-detection fails
- **Status Display**: Shows connection status and port information

#### **Live Detection Panel**
- **Visual Indicator**: Large display showing current classification
  - 🟢 **Green**: No Elephant
  - 🟠 **Orange**: Possible Elephant
  - 🔴 **Red**: ELEPHANT DETECTED! (with audio alert)
- **Classification Details**: Shows classification type and confidence percentage

#### **Audio Features Panel**
- **8 Feature Cards**: Real-time display of audio characteristics
  - 🔊 **RMS Energy**: Overall signal power
  - 🌊 **Infrasound (5-35Hz)**: Low-frequency elephant calls
  - 📊 **Low Band (35-80Hz)**: Mid-range elephant sounds
  - 📉 **Mid Band (80-250Hz)**: Higher-frequency elephant sounds
  - 📈 **Spectral Centroid**: Center of mass of frequency spectrum
  - 🎵 **Dominant Frequency**: Peak frequency component
  - ⏱️ **Temporal Envelope**: Maximum amplitude detection
  - 🌀 **Spectral Flux**: Rate of spectral change

#### **Real-time Plot**
- **Live Visualization**: Shows feature trends over time
- **Multiple Features**: Plot up to 6 features simultaneously
- **Interactive**: Zoom and pan to analyze data
- **Auto-scaling**: Automatically adjusts to data range

#### **Quick Controls**
- **🐘 Label as Elephant**: Mark current sound as elephant
- **🚫 Label as Not Elephant**: Mark current sound as non-elephant
- **💾 Save Data**: Store labeled samples on ESP32
- **🗑️ Clear Data**: Clear all training data
- **📊 Analyze Data**: Switch to analysis tab

### **2. Data Analysis Tab**

#### **Analysis Tools**
- **📊 Feature Distribution**: Statistical analysis of audio features
- **📈 Time Series Analysis**: Trend analysis and pattern recognition
- **🎯 Classification Analysis**: Performance metrics and accuracy
- **💾 Export Data**: Save data in various formats

#### **Visualization Features**
- **Interactive Plots**: Zoom, pan, and analyze data
- **Multiple Chart Types**: Histograms, scatter plots, time series
- **Export Capabilities**: Save plots as images or data as files

### **3. Machine Learning Tab**

#### **Training Tools**
- **🎯 Train Model**: Train custom classification models
- **📊 Test Model**: Validate model performance
- **💾 Save Model**: Store trained models
- **📁 Load Model**: Load previously trained models

#### **Dataset Management**
- **Dataset Information**: Track training data statistics
- **Training Results**: Monitor training progress
- **Model Performance**: View accuracy and metrics

### **4. Settings Tab**

#### **Configuration Options**
- **🎵 Audio Settings**: Adjust sampling and sensitivity
- **🎯 Detection Settings**: Customize classification parameters
- **💻 System Settings**: GUI themes and preferences

## 🔧 **Hardware Setup**

1. **Connect ESP32 to computer via USB**
2. **Connect microphone to GPIO34 (analog input)**
3. **Ensure ESP32 is powered and recognized**
4. **Run the advanced GUI launcher**

## 📊 **System Capabilities**

### **Audio Processing**
- **Sampling Rate**: 1kHz continuous
- **Frame Size**: 256 samples (256ms windows)
- **Features**: 8 optimized audio features
- **Frequency Range**: 5-250Hz (elephant-optimized)
- **Update Rate**: ~1.25 Hz (every 800ms)

### **Real-time Analysis**
- **Live Classification**: Real-time elephant detection
- **Confidence Scoring**: Probability-based classification
- **Visual Alerts**: Color-coded detection indicators
- **Audio Alerts**: Sound notifications for detections

### **Data Management**
- **Labeling**: Mark sounds as elephant/non-elephant
- **Storage**: Save training data to ESP32
- **Export**: Export data in multiple formats
- **Analysis**: Comprehensive data analysis tools

### **Machine Learning**
- **Model Training**: Train custom classification models
- **Performance Testing**: Validate model accuracy
- **Model Management**: Save and load trained models
- **Continuous Learning**: Improve detection over time

## 🎯 **Labeling Data in Advanced GUI**

### **Step 1: Connect to ESP32**
- The system will auto-detect your ESP32
- Status should show "✅ Connected: [PORT]"

### **Step 2: Monitor Real-time Data**
- Watch the audio features update in real-time
- Observe the live plot showing feature trends
- Check the detection panel for classifications

### **Step 3: Label Sounds**
- **For Elephant Sounds**: Click "🐘 Label as Elephant"
- **For Other Sounds**: Click "🚫 Label as Not Elephant"
- **Watch the Status**: Labels are confirmed in the log

### **Step 4: Analyze Data**
- Switch to **Data Analysis** tab
- Use analysis tools to visualize your data
- Export data for further analysis

### **Step 5: Train Models**
- Switch to **Machine Learning** tab
- Click "🎯 Train Model" to train on your labeled data
- Test model performance with "📊 Test Model"

## 🔍 **Troubleshooting**

### **ESP32 Not Detected**
1. Check USB cable connection
2. Verify ESP32 is powered on
3. Install USB drivers if needed
4. Try different USB port

### **No Audio Features**
1. Check microphone connection to GPIO34
2. Verify ESP32 is running correct firmware
3. Try making noise near microphone
4. Check the status log for errors

### **GUI Issues**
1. Make sure all dependencies are installed
2. Check Python version (3.7+ required)
3. Try running from command line to see errors
4. Restart the application

## 📁 **File Structure**

```
📁 Advanced Elephant Detection System/
├── 🚀 run_advanced.bat              # Advanced launcher (Windows)
├── 🐍 launch_advanced_gui.py        # Advanced launcher (Python)
├── 🖼️ python_gui/
│   ├── advanced_elephant_gui.py     # Advanced GUI (NEW)
│   └── simple_elephant_gui.py       # Simple GUI
├── 🔧 esp32_firmware/
│   ├── src/main.cpp                 # Main ESP32 code
│   └── lib/                         # Audio processing libraries
└── 📖 ADVANCED_GUI_README.md        # This file
```

## 🎉 **Success Indicators**

Your advanced system is working correctly when you see:

- ✅ ESP32 connects automatically
- ✅ All 8 audio features display real-time values
- ✅ Live plot shows feature trends
- ✅ Detection panel shows classifications
- ✅ All tabs are functional
- ✅ Data analysis tools work
- ✅ Machine learning features are available

## 🐘 **Ready for Professional Use**

The Advanced Elephant Detection System is now ready for:

1. **Research Applications**: Professional wildlife research
2. **Conservation Projects**: Real-time elephant monitoring
3. **Educational Use**: Teaching AI and machine learning
4. **Field Deployment**: Long-term monitoring systems
5. **Data Analysis**: Comprehensive audio data analysis

**Your advanced elephant detection system is now ready for professional wildlife conservation!** 🌿🐘
