@echo off
echo ========================================
echo Starting AI Employee Watcher (FIXED)
echo ========================================
echo.

REM Set environment variables directly
set DRY_RUN=false
set VAULT_PATH=AI_Employee_Vault
set FILESYSTEM_CHECK_INTERVAL=10

echo Configuration:
echo - DRY_RUN: false (WILL CREATE REAL FILES)
echo - Vault: AI_Employee_Vault (correct spelling)
echo - Watch: test_drops
echo.

REM Check vault exists
if not exist "AI_Employee_Vault\Needs_Action" (
    echo [ERROR] AI_Employee_Vault not found!
    echo Run: create_vault.bat first
    pause
    exit /b 1
)

REM Create test folder if needed
if not exist "test_drops" (
    mkdir test_drops
    echo Created test_drops folder
)

echo ========================================
echo Starting watcher NOW...
echo ========================================
echo.

python filesystem_watcher.py AI_Employee_Vault test_drops

pause
