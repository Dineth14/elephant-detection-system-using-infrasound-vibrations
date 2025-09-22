@echo off
REM Elephant Detection System - Data Analysis Tool Launcher
REM =====================================================

echo.
echo ========================================================
echo    Elephant Detection System - Data Analysis Tool
echo ========================================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7+ and try again
    echo.
    pause
    exit /b 1
)

REM Check if required packages are installed
echo Checking required packages...
python -c "import pandas, numpy, matplotlib, seaborn, sklearn" >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo.
    echo Some required packages are missing. Installing...
    echo Installing: pandas numpy matplotlib seaborn scikit-learn
    pip install pandas numpy matplotlib seaborn scikit-learn
    if %ERRORLEVEL% neq 0 (
        echo ERROR: Failed to install required packages
        echo Please run: pip install pandas numpy matplotlib seaborn scikit-learn
        pause
        exit /b 1
    )
)

echo.
echo Starting Data Analysis Tool...
echo.

REM Run the data analyzer
python data_analyzer.py %*

echo.
echo Analysis completed! Check the 'analysis_results' folder for outputs.
echo.
pause