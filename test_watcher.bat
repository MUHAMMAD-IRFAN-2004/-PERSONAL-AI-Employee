@echo off
echo ========================================
echo Testing AI Employee Watcher
echo ========================================
echo.

REM Check if vault exists
if not exist "AI_Employee_Vault\Needs_Action" (
    echo [ERROR] Vault not found! Run create_vault.bat first.
    pause
    exit /b 1
)

echo [1/4] Vault structure... OK
echo.

REM Check if test_drops exists
if not exist "test_drops" (
    echo Creating test_drops folder...
    mkdir test_drops
)
echo [2/4] Test folder... OK
echo.

REM Create a test file
echo This is a test file for AI Employee > test_drops\test_%date:~-4,4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%.txt
echo [3/4] Test file created in test_drops\
echo.

echo [4/4] Now starting the watcher...
echo.
echo ========================================
echo WATCH THE OUTPUT BELOW:
echo - Should say "DRY_RUN: False"
echo - Should detect the test file
echo - Should create action file
echo ========================================
echo.
echo Press Ctrl+C to stop the watcher
echo.
pause

python filesystem_watcher.py AI_Employee_Vault test_drops
