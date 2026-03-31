@echo off
echo ========================================
echo Quick Test - Drop File and Start
echo ========================================
echo.

REM Set environment directly
set DRY_RUN=false

REM Create test file
echo Test file from AI Employee system > test_drops\quick_test_%random%.txt
echo ✓ Test file created in test_drops\
echo.

echo Starting watcher with DRY_RUN=false...
echo.

python filesystem_watcher.py AI_Employee_Vault test_drops
