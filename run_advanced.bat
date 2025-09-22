@echo off
chcp 65001 >nul
title Advanced Elephant Detection System
color 0A

echo ====================================================
echo    Advanced Elephant Detection System
echo ====================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Display system status
echo [INFO] Python detected: 
python --version

:: Install required packages
echo.
echo [INFO] Installing required packages...
pip install pyserial numpy matplotlib pandas >nul 2>&1

:: Check for ESP32
echo.
echo [INFO] Checking for ESP32 connection...
python -c "import serial.tools.list_ports; ports = [p.device for p in serial.tools.list_ports.comports() if any(k in p.description.upper() for k in ['CP210', 'CH340', 'CH341', 'FTDI', 'USB-SERIAL', 'SILICON LABS', 'ESP32'])]; print('ESP32 ports found:', ports if ports else 'None')"

:: Show usage instructions
echo.
echo ====================================================
echo                 USAGE INSTRUCTIONS
echo ====================================================
echo.
echo 1. Make sure your ESP32 is connected via USB
echo 2. The ESP32 should be running the elephant detection firmware
echo 3. The GUI will auto-detect the ESP32
echo.
echo The Advanced GUI features:
echo   - Real-time elephant detection with visual alerts
echo   - Live audio feature visualization with plots
echo   - Data analysis and machine learning tools
echo   - Advanced labeling and training capabilities
echo   - Export and import functionality
echo   - Multiple tabs for different functions
echo.
echo If the ESP32 is not detected:
echo   - Check USB cable connection
echo   - Verify ESP32 is powered on
echo   - Make sure COM port drivers are installed
echo.

:: Launch the GUI
echo ====================================================
echo [INFO] Starting Advanced Elephant Detection GUI...
echo ====================================================
echo.

:: Run the advanced GUI
python launch_advanced_gui.py

:: Check if GUI closed normally or with error
if errorlevel 1 (
    echo.
    echo [ERROR] GUI closed with an error!
    echo.
    echo Common solutions:
    echo - Check ESP32 connection
    echo - Verify COM port is not used by another application
    echo - Try restarting the system
    echo.
) else (
    echo.
    echo [INFO] GUI closed normally.
)

echo.
echo Press any key to exit...
pause >nul
