@echo off
echo ========================================
echo Checking AI Employee Status
echo ========================================
echo.

echo [Vault Structure]
if exist "AI_Employee_Vault" (
    echo ✓ Vault exists
    if exist "AI_Employee_Vault\Needs_Action" (
        echo ✓ Needs_Action folder exists
        dir /b "AI_Employee_Vault\Needs_Action" | find /c /v "" > temp_count.txt
        set /p file_count=<temp_count.txt
        del temp_count.txt
        echo ✓ Files in Needs_Action: %file_count%
    ) else (
        echo ✗ Needs_Action folder missing!
    )
) else (
    echo ✗ Vault does not exist! Run create_vault.bat first.
)
echo.

echo [Core Files]
if exist "AI_Employee_Vault\Dashboard.md" (
    echo ✓ Dashboard.md exists
) else (
    echo ✗ Dashboard.md missing
)

if exist "AI_Employee_Vault\Company_Handbook.md" (
    echo ✓ Company_Handbook.md exists
) else (
    echo ✗ Company_Handbook.md missing
)

if exist "AI_Employee_Vault\Business_Goals.md" (
    echo ✓ Business_Goals.md exists
) else (
    echo ✗ Business_Goals.md missing
)
echo.

echo [Configuration]
if exist ".env" (
    echo ✓ .env file exists
    findstr /c:"DRY_RUN=false" .env >nul
    if %errorlevel% equ 0 (
        echo ✓ DRY_RUN is set to false
    ) else (
        echo ⚠ DRY_RUN might not be set correctly
    )
) else (
    echo ✗ .env file missing!
)
echo.

echo [Test Folder]
if exist "test_drops" (
    echo ✓ test_drops folder exists
) else (
    echo ⚠ test_drops folder not created yet
)
echo.

echo [Python Dependencies]
python -c "import watchdog; print('✓ watchdog installed')" 2>nul || echo ✗ watchdog not installed
python -c "import dotenv; print('✓ python-dotenv installed')" 2>nul || echo ✗ python-dotenv not installed
echo.

echo ========================================
echo Status Check Complete!
echo ========================================
echo.
echo Ready to test? Run: test_watcher.bat
echo.
pause
