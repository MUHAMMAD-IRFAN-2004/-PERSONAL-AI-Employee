@echo off
echo.
echo ========================================
echo Gmail API Credentials Verification
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Running verification script...
echo.

python verify_credentials.py

echo.
pause
