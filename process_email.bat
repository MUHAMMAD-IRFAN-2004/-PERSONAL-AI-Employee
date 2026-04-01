@echo off
echo ================================================
echo Email Action Helper
echo ================================================
echo.
echo Your email: EMAIL_20260402_042449_greeting.md
echo From: Muhammad Irfan
echo Subject: greeting
echo Message: "hi how are you?"
echo.
echo ================================================
echo What do you want to do?
echo ================================================
echo.
echo 1. View email details
echo 2. Open Gmail to reply
echo 3. Mark as done (move to Done folder)
echo 4. Delete (ignore this email)
echo 5. Exit
echo.
set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" goto view
if "%choice%"=="2" goto gmail
if "%choice%"=="3" goto done
if "%choice%"=="4" goto delete
if "%choice%"=="5" goto end

:view
echo.
echo Opening email file...
notepad "AI_Employee_Vault\Needs_Action\EMAIL_20260402_042449_greeting.md"
echo.
pause
goto end

:gmail
echo.
echo Opening Gmail...
echo Please reply to the email in your browser.
echo.
start https://gmail.com
echo.
echo After replying, run this script again to mark as done.
echo.
pause
goto end

:done
echo.
echo Moving email to Done folder...
if not exist "AI_Employee_Vault\Done" mkdir "AI_Employee_Vault\Done"
move "AI_Employee_Vault\Needs_Action\EMAIL_20260402_042449_greeting.md" "AI_Employee_Vault\Done\" >nul 2>&1
if %errorlevel%==0 (
    echo ✓ Email marked as done!
    echo ✓ File moved to Done folder
) else (
    echo ✗ Error moving file
    echo   File may have already been moved
)
echo.
pause
goto end

:delete
echo.
echo Are you sure you want to delete this email action? (Y/N)
set /p confirm="Confirm: "
if /i "%confirm%"=="Y" (
    del "AI_Employee_Vault\Needs_Action\EMAIL_20260402_042449_greeting.md" >nul 2>&1
    if %errorlevel%==0 (
        echo ✓ Email action deleted
    ) else (
        echo ✗ File not found or already deleted
    )
) else (
    echo Cancelled
)
echo.
pause
goto end

:end
echo.
echo ================================================
echo Email Action Helper - Closed
echo ================================================
