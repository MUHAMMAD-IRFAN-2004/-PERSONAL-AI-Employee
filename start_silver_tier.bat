@echo off
REM ========================================
REM Start Silver Tier Systems
REM ========================================

echo.
echo ========================================
echo STARTING SILVER TIER SYSTEMS
echo ========================================
echo.
echo This will start ALL Bronze and Silver tier watchers:
echo   - Filesystem Watcher (Bronze)
echo   - Gmail Watcher (Bronze)
echo   - WhatsApp Watcher (Silver)
echo   - Approval System (Silver)
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Starting watchers...
echo.

REM Start Filesystem Watcher
echo [1/4] Starting Filesystem Watcher...
start "Filesystem Watcher" cmd /k "echo Starting Filesystem Watcher... && python filesystem_watcher.py AI_Employee_Vault test_drops"
timeout /t 2 /nobreak >nul

REM Start Gmail Watcher
echo [2/4] Starting Gmail Watcher...
start "Gmail Watcher" cmd /k "echo Starting Gmail Watcher... && python gmail_watcher.py"
timeout /t 2 /nobreak >nul

REM Start WhatsApp Watcher
echo [3/4] Starting WhatsApp Watcher...
start "WhatsApp Watcher" cmd /k "echo Starting WhatsApp Watcher... && python whatsapp_watcher.py"
timeout /t 2 /nobreak >nul

REM Start Approval System
echo [4/4] Starting Approval System...
start "Approval System" cmd /k "echo Starting Approval System... && python approval_system.py"
timeout /t 2 /nobreak >nul

echo.
echo ========================================
echo ALL SILVER TIER SYSTEMS STARTED!
echo ========================================
echo.
echo Four windows have been opened:
echo   1. Filesystem Watcher - Monitors folders for new files
echo   2. Gmail Watcher - Monitors Gmail for important emails
echo   3. WhatsApp Watcher - Monitors WhatsApp for messages
echo   4. Approval System - Routes high-risk actions for approval
echo.
echo IMPORTANT: 
echo   - WhatsApp Watcher requires QR code authentication
echo   - Social Poster runs separately: python social_poster.py
echo.
echo To stop all systems, close each window or press Ctrl+C
echo.
echo Check logs in: AI_Employee_Vault\Logs\
echo.
pause
