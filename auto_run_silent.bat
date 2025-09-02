@echo off
title ESP32 Elephant Detection - SILENT MODE
color 0A

echo ==========================================
echo    AUTOMATED ESP32 ELEPHANT DETECTION
echo          SILENT MODE - AUTO CLOSE
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
echo [3/3] Starting GUI in background...
echo.

cd ..
echo ==========================================
echo SUCCESS: ESP32 auto-detected
echo GUI is starting with automatic ESP32 detection...
echo Console will close automatically in 3 seconds...
echo ==========================================

REM Start GUI in background and close console immediately
start "ESP32 GUI" .\.venv\Scripts\python.exe python_gui\noise_logger_gui.py

echo.
echo GUI started! Closing console...
timeout /t 3 /nobreak >nul
exit
