@echo off
echo ================================================
echo Starting Gmail Watcher (PRODUCTION MODE)
echo ================================================
echo.
echo DRY_RUN is set to FALSE
echo Actual files will be created!
echo.
pause

REM Set DRY_RUN environment variable
set DRY_RUN=false

REM Run Gmail Watcher
python gmail_watcher.py

pause
