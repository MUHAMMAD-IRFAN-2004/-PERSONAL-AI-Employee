@echo off
REM Fix Gmail Watcher - Token Expired Issue

echo ========================================
echo Gmail Watcher Token Fix
echo ========================================
echo.
echo Problem: Token has been expired or revoked
echo Solution: Delete old token and re-authenticate
echo.
pause

echo.
echo [1/3] Backing up old token (if exists)...
if exist "token.json" (
    copy token.json token.json.backup >nul
    echo   ✓ Backup created: token.json.backup
) else (
    echo   ! No old token found
)
echo.

echo [2/3] Deleting expired token...
if exist "token.json" (
    del token.json
    echo   ✓ Old token deleted
) else (
    echo   ✓ No token to delete
)
echo.

echo [3/3] Checking credentials.json...
if exist "credentials.json" (
    echo   ✓ credentials.json exists
) else (
    echo   ✗ ERROR: credentials.json not found!
    echo.
    echo   Please ensure credentials.json is in the project folder
    echo   Download from: https://console.cloud.google.com
    pause
    exit /b 1
)
echo.

echo ========================================
echo Token Cleanup Complete!
echo ========================================
echo.
echo Next Steps:
echo.
echo 1. Run Gmail Watcher:
echo    python gmail_watcher.py
echo.
echo 2. Browser will open automatically
echo.
echo 3. Login to your Google account
echo.
echo 4. Click "Allow" to grant permissions
echo.
echo 5. New token.json will be created
echo.
echo 6. Gmail Watcher will start working!
echo.
echo Starting Gmail Watcher now...
echo.
pause

python gmail_watcher.py

pause
