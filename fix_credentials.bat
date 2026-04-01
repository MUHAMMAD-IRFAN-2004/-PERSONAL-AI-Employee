@echo off
REM Quick Fix for Social Poster Credentials Issue

echo ========================================
echo Social Poster - Credentials Fix
echo ========================================
echo.

echo Problem dekha:
echo   - LinkedIn credentials missing
echo   - Twitter credentials missing  
echo   - README.md galti se queue mein
echo.
echo Sab theek karte hain...
echo.
pause

echo.
echo [1/4] Social_Queue cleanup...
echo.

REM Remove README.md from queue if exists
if exist "AI_Employee_Vault\Social_Queue\README.md" (
    echo   Removing README.md from queue...
    del "AI_Employee_Vault\Social_Queue\README.md"
    echo   ✓ Done
) else (
    echo   ✓ README.md already removed
)

REM Clean Failed folder
if exist "AI_Employee_Vault\Social_Queue\Failed\README.md" (
    echo   Removing README.md from Failed folder...
    del "AI_Employee_Vault\Social_Queue\Failed\README.md"
    echo   ✓ Done
)

echo.
echo [2/4] Checking .env file...
echo.

if not exist ".env" (
    echo   Creating .env from template...
    copy .env.example .env >nul
    echo   ✓ .env created
) else (
    echo   ✓ .env exists
)

echo.
echo [3/4] Opening .env for editing...
echo.
echo IMPORTANT: Ye karo .env file mein:
echo.
echo 1. LinkedIn credentials add karo:
echo    LINKEDIN_EMAIL=your.email@example.com
echo    LINKEDIN_PASSWORD=your_password_here
echo.
echo 2. Twitter lines ko comment karo (# lagao):
echo    # TWITTER_USERNAME=
echo    # TWITTER_PASSWORD=
echo.
echo 3. Save karo (Ctrl+S) aur close karo
echo.
pause

notepad .env

echo.
echo [4/4] Verifying credentials...
echo.

findstr /i "LINKEDIN_EMAIL" .env >nul
if errorlevel 1 (
    echo   ✗ LINKEDIN_EMAIL not found in .env
    echo     Please add: LINKEDIN_EMAIL=your.email@example.com
) else (
    echo   ✓ LINKEDIN_EMAIL found
)

findstr /i "LINKEDIN_PASSWORD" .env >nul
if errorlevel 1 (
    echo   ✗ LINKEDIN_PASSWORD not found in .env
    echo     Please add: LINKEDIN_PASSWORD=your_password
) else (
    echo   ✓ LINKEDIN_PASSWORD found
)

echo.
echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Ab ye karo:
echo.
echo 1. Test credentials:
echo    python verify_credentials.py
echo.
echo 2. Nayi post banao:
echo    post_linkedin_only.bat
echo.
echo 3. Social poster chalao:
echo    python social_poster.py
echo.
pause
