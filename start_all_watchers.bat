@echo off
REM ========================================
REM Start All Watchers - Bronze + Silver Tier
REM ========================================

echo.
echo ========================================
echo STARTING ALL WATCHERS
echo ========================================
echo.

REM Start Filesystem Watcher (Bronze)
echo [1/3] Starting Filesystem Watcher...
start "Filesystem Watcher" cmd /k python filesystem_watcher.py AI_Employee_Vault test_drops
timeout /t 2 /nobreak >nul

REM Start Gmail Watcher (Bronze)
echo [2/3] Starting Gmail Watcher...
start "Gmail Watcher" cmd /k python gmail_watcher.py
timeout /t 2 /nobreak >nul

REM Start WhatsApp Watcher (Silver)
echo [3/3] Starting WhatsApp Watcher...
start "WhatsApp Watcher" cmd /k python whatsapp_watcher.py
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ALL WATCHERS STARTED!
echo ========================================
echo.
echo Three windows have been opened:
echo   1. Filesystem Watcher - Monitors AI_Employee_Vault and test_drops
echo   2. Gmail Watcher - Monitors your Gmail inbox
echo   3. WhatsApp Watcher - Monitors WhatsApp Web messages
echo.
echo To stop a watcher, close its window or press Ctrl+C
echo.
pause
