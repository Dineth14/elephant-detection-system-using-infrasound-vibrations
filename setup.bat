@echo off
title ESP32 Elephant Detection System - Setup
color 0B

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo ==========================================
echo  ESP32 ELEPHANT DETECTION SYSTEM
echo              Setup
echo ==========================================
echo.
echo Creating Python virtual environment...

python -m venv .venv
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment. Make sure Python is installed.
    pause
    exit /b 1
)

echo.
echo Installing required packages...
".venv\Scripts\python.exe" -m pip install --upgrade pip
".venv\Scripts\python.exe" -m pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [ERROR] Failed to install packages.
    pause
    exit /b 1
)

echo.
echo [SUCCESS] Setup complete!
echo.
echo To launch the GUI:
echo   * Double-click: run_gui.bat
echo   * Or run: python python_gui/noise_logger_gui.py  
echo.
pause
