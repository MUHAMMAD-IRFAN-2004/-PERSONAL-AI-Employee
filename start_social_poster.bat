@echo off
REM ========================================
REM Social Media Poster Launcher
REM ========================================

echo.
echo ========================================
echo SOCIAL MEDIA POSTER
echo ========================================
echo.
echo This will start the social media posting system.
echo.
echo What it does:
echo   - Monitors Social_Queue/ folder
echo   - Posts to LinkedIn and Twitter
echo   - Respects rate limits (5 LinkedIn, 10 Twitter/day)
echo   - Saves sessions for easy re-login
echo.
echo REQUIREMENTS:
echo   1. LinkedIn/Twitter credentials in .env file
echo   2. Post files in Social_Queue/ folder
echo   3. Playwright and Chromium installed
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Checking prerequisites...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not installed!
    pause
    exit /b 1
)
echo [OK] Python installed

REM Check Playwright
python -c "import playwright" >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Playwright not installed!
    echo Run: pip install playwright
    echo Then: playwright install chromium
    pause
    exit /b 1
)
echo [OK] Playwright installed

REM Check .env exists
if not exist ".env" (
    echo [WARNING] .env file not found!
    echo Creating from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env and add your LinkedIn/Twitter credentials!
    echo.
    pause
)

REM Check Social_Queue exists
if not exist "AI_Employee_Vault\Social_Queue" (
    echo [ERROR] Social_Queue folder not found!
    echo Creating it now...
    call create_social_queue_v2.bat
)
echo [OK] Social_Queue folder exists

REM Check if any posts in queue
dir "AI_Employee_Vault\Social_Queue\*.md" >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [INFO] No posts in queue yet
    echo.
    echo Create a post file in: AI_Employee_Vault\Social_Queue\
    echo.
    echo Example:
    echo   post_to_linkedin.bat
    echo.
    set /p "create=Create a test post now? (y/n): "
    if /i "%create%"=="y" (
        call post_to_linkedin.bat
    )
)

echo.
echo ========================================
echo Starting Social Media Poster...
echo ========================================
echo.
echo Browser will open for first-time login.
echo Sessions saved for future runs.
echo.
echo Press Ctrl+C to stop
echo.

python social_poster.py

pause
