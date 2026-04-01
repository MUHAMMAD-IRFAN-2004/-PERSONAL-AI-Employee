@echo off
echo ========================================
echo Blank Page Issue - Quick Fix
echo ========================================
echo.
echo Ye script blank page issue fix karega
echo.
pause

echo.
echo [Step 1/5] Browser session clear kar rahe hain...
if exist ".social_browser_data" (
    rmdir /s /q .social_browser_data
    echo   Done - Purana session data deleted
) else (
    echo   No old session found
)
echo.

echo [Step 2/5] Rate limit file clear kar rahe hain...
if exist "AI_Employee_Vault\.social_rate_limits.json" (
    del AI_Employee_Vault\.social_rate_limits.json
    echo   Done - Rate limit reset
) else (
    echo   No rate limit file found
)
echo.

echo [Step 3/5] Chromium reinstall kar rahe hain...
echo   This may take a few minutes...
playwright install chromium --force
echo.

echo [Step 4/5] Testing browser...
python test_browser.py
echo.

echo [Step 5/5] .env file check
if exist ".env" (
    echo   .env file exists
    echo.
    echo   Checking critical settings...
    findstr /i "SOCIAL_HEADLESS" .env >nul
    if errorlevel 1 (
        echo   Adding SOCIAL_HEADLESS=false
        echo SOCIAL_HEADLESS=false >> .env
    ) else (
        echo   SOCIAL_HEADLESS setting found
    )
    
    findstr /i "LINKEDIN_EMAIL" .env >nul
    if errorlevel 1 (
        echo   WARNING: LINKEDIN_EMAIL not set in .env
    ) else (
        echo   LINKEDIN_EMAIL is set
    )
) else (
    echo   ERROR: .env file not found!
    echo   Creating from template...
    copy .env.example .env
    echo.
    echo   Please edit .env and add your credentials!
    notepad .env
)
echo.

echo ========================================
echo Fixes Applied!
echo ========================================
echo.
echo Ab try karo:
echo   python social_poster.py
echo.
echo Agar phir bhi blank page aaye to:
echo   1. Browser console dekho (F12)
echo   2. Internet connection check karo
echo   3. Antivirus disable karke try karo
echo.
pause
