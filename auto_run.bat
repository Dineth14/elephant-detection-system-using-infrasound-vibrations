@echo off
title ESP32 Elephant Detection - AUTOMATED
color 0A

echo ==========================================
echo    AUTOMATED ESP32 ELEPHANT DETECTION
echo ==========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [1/3] Uploading ESP32 firmware...
cd esp32_firmware
..\.venv\Scripts\python.exe -m platformio run --target upload
if %errorlevel% neq 0 (
    echo [ERROR] ESP32 upload failed!
    pause
    exit /b 1
)

echo.
echo [2/3] ESP32 firmware uploaded successfully!
echo [3/3] Starting GUI...
echo.

cd ..
echo.
echo [2/3] ESP32 firmware uploaded successfully!
echo [3/3] Starting GUI...
echo.
echo ==========================================
echo SUCCESS: ESP32 auto-detected
echo GUI is starting with automatic ESP32 detection...
echo The system will automatically find and connect to your ESP32
echo No manual port selection needed!
echo ==========================================
echo.
echo Starting GUI... (Console will close automatically when GUI closes)

REM Start GUI and wait for it to close, then automatically close console
.\.venv\Scripts\python.exe python_gui\noise_logger_gui.py

echo.
echo GUI closed. Exiting...
timeout /t 2 /nobreak >nul
exit
