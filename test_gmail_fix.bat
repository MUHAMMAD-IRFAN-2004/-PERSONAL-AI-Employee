@echo off
echo ================================================
echo Testing Gmail Watcher with Fixed DRY_RUN
echo ================================================
echo.
echo Starting Gmail Watcher...
echo Press Ctrl+C after 10 seconds to check output
echo.
timeout /t 3
python gmail_watcher.py
