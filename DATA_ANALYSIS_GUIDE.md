# Data Analysis Tool - User Guide

## Overview

The Elephant Detection System Data Analysis Tool provides comprehensive visualization and statistical analysis of logged data from the ESP32 elephant detection system. It offers multiple visualization techniques including time-series analysis, Principal Component Analysis (PCA), correlation matrices, and detailed statistical summaries.

## Features

### 🔍 **Comprehensive Analysis Options**
- **Feature Time-series**: Visualize how all 8 audio features change over time
- **PCA Analysis**: Reduce dimensionality and visualize feature relationships
- **Correlation Analysis**: Understand relationships between different features
- **Detection Analysis**: Analyze detection patterns and confidence scores
- **Statistical Summary**: Comprehensive statistics and distributions

### 📊 **Visualizations Included**

#### 1. Feature Time-Series Analysis
- Plots all 8 audio features over time
- Highlights elephant detection events in red
- Shows feature behavior patterns
- Saves as `feature_timeseries.png`

#### 2. Principal Component Analysis (PCA)
- **Explained Variance**: Shows how much variance each component explains
- **2D PCA Plot**: First two principal components with detection highlighting
- **3D PCA Plot**: Three-dimensional view of feature space
- **Feature Loadings**: Biplot showing feature contributions to components
- Saves as `pca_analysis.png`

#### 3. Correlation Matrix
- **Heatmap**: Color-coded correlation matrix between all features
- **Network Graph**: Visualizes strong correlations (|r| ≥ 0.5)
- Saves as `correlation_analysis.png`

#### 4. Detection Analysis
- **Detection Timeline**: When detections occurred
- **Confidence Distribution**: Histogram of confidence scores
- **Hourly Detection Rate**: Detection frequency by hour of day
- **Feature Comparison**: Normal vs detection feature values
- Saves as `detection_analysis.png`

#### 5. Statistical Summary
- **Feature Distributions**: Histograms with KDE curves for each feature
- **Statistics Table**: Mean, std, min, max, percentiles, skewness, kurtosis
- Saves as `statistical_summary.png`

## Quick Start

### Method 1: Using the Launcher (Recommended)
```batch
# Double-click or run:
run_data_analysis.bat
```

### Method 2: Command Line
```bash
# Install dependencies
pip install -r data_analysis_requirements.txt

# Run with sample data
python data_analyzer.py --sample

# Run with your data file
python data_analyzer.py --file your_data.csv
```

### Method 3: Generate Sample Data First
```bash
# Generate sample data
python generate_sample_data.py --samples 5000 --output sample_data.csv

# Analyze the generated data
python data_analyzer.py --file sample_data.csv
```

## Input Data Formats

The tool supports multiple data formats:

### 1. CSV Format
```csv
timestamp,rms,zcr,energy,spectral_centroid,spectral_rolloff,mfcc1,mfcc2,mfcc3,detection,confidence
2025-01-01 00:00:00,0.023,0.145,0.001,245.2,487.3,-2.1,0.8,-0.3,0,0.0
2025-01-01 00:00:01,0.087,0.132,0.007,198.7,321.5,-1.8,1.2,-0.1,1,0.85
```

### 2. JSON Format
```json
[
  {
    "timestamp": "2025-01-01 00:00:00",
    "rms": 0.023,
    "zcr": 0.145,
    "energy": 0.001,
    "spectral_centroid": 245.2,
    "spectral_rolloff": 487.3,
    "mfcc1": -2.1,
    "mfcc2": 0.8,
    "mfcc3": -0.3,
    "detection": 0,
    "confidence": 0.0
  }
]
```

### 3. ESP32 Serial Log Format
```
# ESP32 Elephant Detection System Data Log
2025-01-01 00:00:00,0.023,0.145,0.001,245.2,487.3,-2.1,0.8,-0.3,0,0.0
2025-01-01 00:00:01,0.087,0.132,0.007,198.7,321.5,-1.8,1.2,-0.1,1,0.85
```

## Command Line Options

```bash
python data_analyzer.py [options]

Options:
  -h, --help          Show help message
  -f, --file FILE     Path to data file
  -s, --sample        Generate sample data for demonstration
  -o, --output DIR    Output directory for results (default: analysis_results)
```

## Interactive Menu

When run without arguments, the tool provides an interactive menu:

```
Available Analysis Options:
1. Complete Analysis (All visualizations)
2. Feature Time-series Only
3. PCA Analysis Only
4. Correlation Analysis Only
5. Detection Analysis Only
6. Statistical Summary Only

Enter your choice (1-6) or press Enter for complete analysis:
```

## Output Files

All results are saved in the `analysis_results` directory:

- **`feature_timeseries.png`** - Time-series plots of all features
- **`pca_analysis.png`** - PCA analysis with multiple views
- **`correlation_analysis.png`** - Correlation matrix and network
- **`detection_analysis.png`** - Detection patterns and confidence
- **`statistical_summary.png`** - Comprehensive statistics
- **`analysis_report.txt`** - Text summary report

## Feature Descriptions

### Audio Features Analyzed

1. **RMS (Root Mean Square)** - Overall amplitude/loudness
2. **ZCR (Zero Crossing Rate)** - Rate of signal sign changes
3. **Energy** - Total energy of the signal
4. **Spectral Centroid** - Center of mass of spectrum
5. **Spectral Rolloff** - Frequency below which 85% of energy lies
6. **MFCC1-3** - First three Mel-Frequency Cepstral Coefficients

### Detection Information
- **Detection** - Binary flag (0=normal, 1=elephant detected)
- **Confidence** - Classification confidence score (0.0-1.0)

## Installation Requirements

### Core Dependencies
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

### Or use the requirements file:
```bash
pip install -r data_analysis_requirements.txt
```

## Sample Data Generation

Generate realistic test data for analysis:

```bash
# Generate 5000 samples with 3% detection rate
python generate_sample_data.py --samples 5000 --detections 0.03 --output test_data.csv

# Generate data in different formats
python generate_sample_data.py --format json --output data.json
python generate_sample_data.py --format log --output data.log
```

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   ```bash
   pip install -r data_analysis_requirements.txt
   ```

2. **Invalid Data Format**
   - Check that your data has the required columns
   - Use the sample data generator to create test data
   - Ensure timestamps are in a readable format

3. **Memory Issues with Large Datasets**
   - The tool can handle datasets with 100,000+ samples
   - For very large files (>1M samples), consider sampling your data first

4. **Display Issues**
   - If plots don't show, make sure you have a display available
   - On headless systems, plots are still saved to files

### Getting Help

If you encounter issues:

1. Check the `analysis_report.txt` for data summary information
2. Run with sample data first: `python data_analyzer.py --sample`
3. Verify your data format matches one of the supported formats
4. Check that all required columns are present in your data

## Advanced Usage

### Programmatic Usage

```python
from data_analyzer import DataAnalyzer

# Create analyzer
analyzer = DataAnalyzer()

# Load your data
analyzer.load_data("your_data.csv")

# Run specific analyses
analyzer.plot_feature_timeseries()
pca_components = analyzer.perform_pca_analysis()
analyzer.plot_correlation_matrix()
analyzer.plot_detection_analysis()
analyzer.plot_statistical_summary()

# Or run everything
analyzer.run_complete_analysis()
```

### Customization

You can modify the `DataAnalyzer` class to:
- Add new visualization types
- Change color schemes or plot styles
- Implement additional statistical tests
- Add custom feature engineering

## Performance Notes

- **Small datasets** (< 1,000 samples): Analysis completes in seconds
- **Medium datasets** (1,000 - 50,000 samples): Analysis takes 10-30 seconds
- **Large datasets** (> 50,000 samples): May take 1-2 minutes for complete analysis

The tool is optimized for typical elephant detection monitoring scenarios where data is collected over hours to days.

---

**Author**: Elephant Detection System Project  
**Version**: 1.0  
**Last Updated**: September 2025