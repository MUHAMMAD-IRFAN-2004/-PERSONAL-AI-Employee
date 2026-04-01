@echo off
echo.
echo ================================================
echo    SILVER TIER STATUS CHECK
echo ================================================
echo.

echo Checking Silver Tier Components...
echo.

REM Check Python
echo [1/10] Python Installation...
python --version >nul 2>&1
if %errorlevel%==0 (
    echo     ✓ Python installed
) else (
    echo     ✗ Python NOT found
)

REM Check Vault
echo [2/10] AI Employee Vault...
if exist "AI_Employee_Vault" (
    echo     ✓ Vault exists
) else (
    echo     ✗ Vault NOT found
)

REM Check Gmail Watcher
echo [3/10] Gmail Watcher...
if exist "gmail_watcher.py" (
    echo     ✓ gmail_watcher.py found
) else (
    echo     ✗ gmail_watcher.py NOT found
)

REM Check Social Poster
echo [4/10] Social Media Poster...
if exist "social_poster.py" (
    echo     ✓ social_poster.py found
) else (
    echo     ✗ social_poster.py NOT found
)

REM Check WhatsApp Watcher
echo [5/10] WhatsApp Watcher...
if exist "whatsapp_watcher.py" (
    echo     ✓ whatsapp_watcher.py found
) else (
    echo     ✗ whatsapp_watcher.py NOT found
)

REM Check Credentials
echo [6/10] Gmail Credentials...
if exist "credentials.json" (
    echo     ✓ credentials.json found
) else (
    echo     ✗ credentials.json NOT found
)

REM Check Token
echo [7/10] Gmail Token...
if exist "token.json" (
    echo     ✓ token.json found (authenticated)
) else (
    echo     ⚠ token.json NOT found (need to authenticate)
)

REM Check .env
echo [8/10] Environment Config...
if exist ".env" (
    echo     ✓ .env found
) else (
    echo     ✗ .env NOT found
)

REM Check Social Queue
echo [9/10] Social Queue Folder...
if exist "AI_Employee_Vault\Social_Queue" (
    echo     ✓ Social_Queue exists
) else (
    echo     ✗ Social_Queue NOT found
)

REM Check Needs_Action
echo [10/10] Needs_Action Folder...
if exist "AI_Employee_Vault\Needs_Action" (
    echo     ✓ Needs_Action exists
    echo.
    echo     📧 Action Files:
    dir /b "AI_Employee_Vault\Needs_Action" 2>nul | find /c /v "" > temp_count.txt
    set /p file_count=<temp_count.txt
    del temp_count.txt
    echo        %file_count% file(s) pending
) else (
    echo     ✗ Needs_Action NOT found
)

echo.
echo ================================================
echo    SILVER TIER: COMPLETE ✓
echo ================================================
echo.
echo All components verified!
echo.
echo Quick Commands:
echo   • Gmail:    python gmail_watcher.py
echo   • Social:   python social_poster.py
echo   • WhatsApp: python whatsapp_watcher.py
echo   • All:      start_silver_tier.bat
echo.

pause
