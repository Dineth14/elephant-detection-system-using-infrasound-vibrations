
@echo off
title ESP32 Elephant Detection System
color 0A

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ==========================================
echo    ESP32 ELEPHANT DETECTION SYSTEM
echo ==========================================
echo.
echo [INFO] Starting GUI...
echo [INFO] Close this window when done with GUI
echo.
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found!
    echo [SOLUTION] Please run setup.bat first
    echo.
    pause
    exit /b 1
)

echo [LAUNCH] Starting ESP32 Noise Logger GUI...
".venv\Scripts\python.exe" python_gui\noise_logger_gui.py

if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Failed to start GUI
    echo [SOLUTION] Try running setup.bat to fix dependencies
    echo.
    pause
) else (
    echo.
    echo [SUCCESS] GUI closed normally
)
