@echo off
REM ========================================
REM Silver Tier Setup Script
REM ========================================

echo.
echo ========================================
echo SILVER TIER SETUP
echo ========================================
echo.

REM Check Python
echo [1/6] Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
python --version

echo.
echo [2/6] Installing Python dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [3/6] Installing Playwright browsers...
playwright install chromium
if %errorlevel% neq 0 (
    echo WARNING: Playwright installation had issues
    echo You may need to run: playwright install chromium
    pause
)

echo.
echo [4/6] Creating directory structure...
call create_social_queue.bat

REM Create other missing directories
if not exist "AI_Employee_Vault\Pending_Approval" mkdir "AI_Employee_Vault\Pending_Approval"
if not exist "AI_Employee_Vault\Approved" mkdir "AI_Employee_Vault\Approved"
if not exist "AI_Employee_Vault\Rejected" mkdir "AI_Employee_Vault\Rejected"

echo.
echo [5/6] Setting up environment file...
if not exist ".env" (
    copy .env.example .env
    echo Created .env file from template
    echo IMPORTANT: Edit .env and add your credentials!
) else (
    echo .env file already exists
)

echo.
echo [6/6] Running status check...
call check_silver_status.bat

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo   1. Edit .env file with your credentials:
echo      - LINKEDIN_EMAIL and LINKEDIN_PASSWORD
echo      - TWITTER_USERNAME and TWITTER_PASSWORD
echo      - WHATSAPP_PRIORITY_SENDERS (optional)
echo.
echo   2. Start Silver Tier systems:
echo      start_silver_tier.bat
echo.
echo   3. Read the guide:
echo      SILVER_TIER_GUIDE.md
echo.
pause
