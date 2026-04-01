@echo off
REM Fix for Twitter Auto-Opening Issue

echo ========================================
echo Fix: Twitter Automatic Khulna Band Karo
echo ========================================
echo.
echo Ye script Twitter ko automatic khulne se rokegi
echo.
pause

echo.
echo [Step 1/4] .env file backup bana rahe hain...
if exist ".env" (
    copy .env .env.backup >nul
    echo   ✓ Backup created: .env.backup
) else (
    echo   ! .env file nahi mili
)
echo.

echo [Step 2/4] Twitter credentials ko disable kar rahe hain...
if exist ".env" (
    REM Create temporary file without Twitter credentials
    findstr /v /i "TWITTER_USERNAME TWITTER_PASSWORD" .env > .env.temp
    
    REM Add commented Twitter settings
    echo. >> .env.temp
    echo # Twitter Settings - DISABLED >> .env.temp
    echo # Uncomment ye lines agar Twitter bhi use karna ho >> .env.temp
    echo # TWITTER_USERNAME= >> .env.temp
    echo # TWITTER_PASSWORD= >> .env.temp
    
    REM Replace original with temp
    move /y .env.temp .env >nul
    echo   ✓ Twitter credentials disabled
) else (
    echo   ! .env file process nahi hui
)
echo.

echo [Step 3/4] Browser session clear kar rahe hain...
if exist ".social_browser_data" (
    rmdir /s /q .social_browser_data
    echo   ✓ Browser session cleared
) else (
    echo   ✓ No old session to clear
)
echo.

echo [Step 4/4] Old posts queue se hata rahe hain (optional)...
set /p clearqueue="Queue clear karna hai? Purani posts delete ho jayengi (y/n): "
if /i "%clearqueue%"=="y" (
    del AI_Employee_Vault\Social_Queue\*.md 2>nul
    echo   ✓ Queue cleared
) else (
    echo   ✓ Queue preserved
)
echo.

echo ========================================
echo Fix Complete!
echo ========================================
echo.
echo Changes applied:
echo   1. .env backup banaya
echo   2. Twitter credentials disabled
echo   3. Browser session cleared
echo   4. Queue cleared (agar select kiya)
echo.
echo Ab kya karein:
echo.
echo   1. Nayi LinkedIn post banao:
echo      post_linkedin_only.bat
echo.
echo   2. Social poster chalao:
echo      python social_poster.py
echo.
echo   3. Result:
echo      Sirf LinkedIn khulega ✓
echo      Twitter NAHI khulega ✓
echo.
echo Agar dobara Twitter use karna ho:
echo   .env.backup se restore karo
echo.
pause
