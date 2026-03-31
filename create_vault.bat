@echo off
REM AI Employee Vault Directory Structure Creation Script
REM This script creates the complete vault directory structure

setlocal enabledelayedexpansion

set "VAULT_PATH=D:\PIAIC AI\-PERSONAL-AI-Employee\AI_Employee_Vault"

echo Creating AI Employee Vault Directory Structure...
echo.

REM Create base vault directory
mkdir "%VAULT_PATH%" 2>nul
echo.

REM Create all subdirectories
mkdir "%VAULT_PATH%\Inbox"
echo [SUCCESS] Inbox created

mkdir "%VAULT_PATH%\Needs_Action"
echo [SUCCESS] Needs_Action created

mkdir "%VAULT_PATH%\In_Progress"
echo [SUCCESS] In_Progress created

mkdir "%VAULT_PATH%\Done"
echo [SUCCESS] Done created

mkdir "%VAULT_PATH%\Pending_Approval"
echo [SUCCESS] Pending_Approval created

mkdir "%VAULT_PATH%\Approved"
echo [SUCCESS] Approved created

mkdir "%VAULT_PATH%\Rejected"
echo [SUCCESS] Rejected created

mkdir "%VAULT_PATH%\Plans"
echo [SUCCESS] Plans created

mkdir "%VAULT_PATH%\Briefings"
echo [SUCCESS] Briefings created

mkdir "%VAULT_PATH%\Logs"
echo [SUCCESS] Logs created

mkdir "%VAULT_PATH%\Accounting"
echo [SUCCESS] Accounting created

mkdir "%VAULT_PATH%\Active_Project"
echo [SUCCESS] Active_Project created

echo.
echo ========================================
echo Directory structure creation complete!
echo ========================================
echo.
echo Vault location: %VAULT_PATH%
echo.
echo Verifying directory structure...
dir "%VAULT_PATH%"
pause
