@echo off
REM Navigation Helper - Open Key Documentation Files
REM Double-click to see menu of important files

echo ========================================
echo   Personal AI Employee - File Navigator
echo ========================================
echo.
echo Choose a file to open:
echo.
echo [1] 00_START_HERE.md        - Quick start guide
echo [2] PROJECT_STRUCTURE.md    - Organized file list
echo [3] FILE_INDEX.md           - Alphabetical index
echo [4] README.md               - Full documentation
echo [5] Company_Handbook.md     - Configure AI rules
echo [6] Business_Goals.md       - Set objectives
echo [7] filesystem_watcher.log  - Check logs
echo [8] .env                     - Edit credentials
echo.
echo [9] Open AI_Employee_Vault folder
echo.
echo [0] Exit
echo.

set /p choice="Enter your choice (0-9): "

if "%choice%"=="1" start notepad "00_START_HERE.md"
if "%choice%"=="2" start notepad "PROJECT_STRUCTURE.md"
if "%choice%"=="3" start notepad "FILE_INDEX.md"
if "%choice%"=="4" start notepad "README.md"
if "%choice%"=="5" start notepad "Company_Handbook.md"
if "%choice%"=="6" start notepad "Business_Goals.md"
if "%choice%"=="7" start notepad "filesystem_watcher.log"
if "%choice%"=="8" start notepad ".env"
if "%choice%"=="9" start explorer "AI_Employee_Vault"
if "%choice%"=="0" exit

echo.
echo File opened! Press any key to see menu again...
pause >nul
goto :start
