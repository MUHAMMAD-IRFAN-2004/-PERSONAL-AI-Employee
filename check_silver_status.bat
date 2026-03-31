@echo off
REM ========================================
REM Check Silver Tier Status
REM ========================================

echo.
echo ========================================
echo SILVER TIER STATUS CHECK
echo ========================================
echo.

REM Check if Python is installed
echo Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    goto :end
) else (
    python --version
    echo [OK] Python is installed
)
echo.

REM Check if required packages are installed
echo Checking required packages...
echo.

echo Checking playwright...
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] playwright not installed - Run: pip install playwright
    echo         Then run: playwright install chromium
) else (
    echo [OK] playwright installed
)

echo Checking watchdog...
python -c "import watchdog" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] watchdog not installed - Run: pip install watchdog
) else (
    echo [OK] watchdog installed
)

echo Checking google-api-python-client...
python -c "import googleapiclient" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] google-api-python-client not installed
    echo         Run: pip install google-api-python-client google-auth google-auth-oauthlib
) else (
    echo [OK] google-api-python-client installed
)

echo Checking python-dotenv...
python -c "import dotenv" >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] python-dotenv not installed - Run: pip install python-dotenv
) else (
    echo [OK] python-dotenv installed
)

echo.

REM Check if directories exist
echo Checking directory structure...
echo.

if exist "AI_Employee_Vault\" (
    echo [OK] AI_Employee_Vault directory exists
) else (
    echo [ERROR] AI_Employee_Vault directory missing!
)

if exist "AI_Employee_Vault\Needs_Action\" (
    echo [OK] Needs_Action directory exists
) else (
    echo [WARNING] Needs_Action directory missing
)

if exist "AI_Employee_Vault\Pending_Approval\" (
    echo [OK] Pending_Approval directory exists
) else (
    echo [WARNING] Pending_Approval directory missing
)

if exist "AI_Employee_Vault\Approved\" (
    echo [OK] Approved directory exists
) else (
    echo [WARNING] Approved directory missing
)

if exist "AI_Employee_Vault\Rejected\" (
    echo [OK] Rejected directory exists
) else (
    echo [WARNING] Rejected directory missing
)

if exist "AI_Employee_Vault\Logs\" (
    echo [OK] Logs directory exists
) else (
    echo [WARNING] Logs directory missing
)

echo.

REM Check if Python scripts exist
echo Checking Python scripts...
echo.

if exist "filesystem_watcher.py" (
    echo [OK] filesystem_watcher.py exists
) else (
    echo [ERROR] filesystem_watcher.py missing!
)

if exist "gmail_watcher.py" (
    echo [OK] gmail_watcher.py exists
) else (
    echo [ERROR] gmail_watcher.py missing!
)

if exist "whatsapp_watcher.py" (
    echo [OK] whatsapp_watcher.py exists
) else (
    echo [ERROR] whatsapp_watcher.py missing!
)

if exist "approval_system.py" (
    echo [OK] approval_system.py exists
) else (
    echo [ERROR] approval_system.py missing!
)

if exist "social_poster.py" (
    echo [OK] social_poster.py exists
) else (
    echo [ERROR] social_poster.py missing!
)

echo.

REM Check environment file
echo Checking environment configuration...
echo.

if exist ".env" (
    echo [OK] .env file exists
    echo Check that it contains:
    echo   - LINKEDIN_EMAIL and LINKEDIN_PASSWORD
    echo   - TWITTER_USERNAME and TWITTER_PASSWORD
    echo   - WhatsApp settings (optional)
) else (
    echo [WARNING] .env file missing
    echo Copy .env.example to .env and configure
)

echo.

REM Check running processes
echo Checking for running watchers...
echo.

tasklist /FI "WINDOWTITLE eq Filesystem Watcher" 2>nul | find "python.exe" >nul
if %errorlevel% equ 0 (
    echo [RUNNING] Filesystem Watcher
) else (
    echo [STOPPED] Filesystem Watcher
)

tasklist /FI "WINDOWTITLE eq Gmail Watcher" 2>nul | find "python.exe" >nul
if %errorlevel% equ 0 (
    echo [RUNNING] Gmail Watcher
) else (
    echo [STOPPED] Gmail Watcher
)

tasklist /FI "WINDOWTITLE eq WhatsApp Watcher" 2>nul | find "python.exe" >nul
if %errorlevel% equ 0 (
    echo [RUNNING] WhatsApp Watcher
) else (
    echo [STOPPED] WhatsApp Watcher
)

tasklist /FI "WINDOWTITLE eq Approval System" 2>nul | find "python.exe" >nul
if %errorlevel% equ 0 (
    echo [RUNNING] Approval System
) else (
    echo [STOPPED] Approval System
)

echo.

REM Check recent logs
echo Checking recent logs...
echo.

if exist "AI_Employee_Vault\Logs\" (
    echo Most recent log files:
    dir /B /O-D /TW "AI_Employee_Vault\Logs\*.log" 2>nul | findstr /R ".*" >nul
    if %errorlevel% equ 0 (
        dir /B /O-D /TW "AI_Employee_Vault\Logs\*.log" 2>nul | more +0
    ) else (
        echo No log files found
    )
) else (
    echo Logs directory does not exist
)

echo.

:end
echo ========================================
echo STATUS CHECK COMPLETE
echo ========================================
echo.
echo To start Silver Tier: run start_silver_tier.bat
echo To view logs: check AI_Employee_Vault\Logs\
echo.
pause
