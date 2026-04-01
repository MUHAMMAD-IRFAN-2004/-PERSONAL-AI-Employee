@echo off
echo Creating Silver Tier Skill Directories...
echo.

cd /d "%~dp0"

mkdir ".agents\skills\whatsapp-monitor" 2>nul
if exist ".agents\skills\whatsapp-monitor" (
    echo [OK] Created whatsapp-monitor
) else (
    echo [ERROR] Failed to create whatsapp-monitor
)

mkdir ".agents\skills\approval-workflow" 2>nul
if exist ".agents\skills\approval-workflow" (
    echo [OK] Created approval-workflow
) else (
    echo [ERROR] Failed to create approval-workflow
)

mkdir ".agents\skills\social-media-poster" 2>nul
if exist ".agents\skills\social-media-poster" (
    echo [OK] Created social-media-poster
) else (
    echo [ERROR] Failed to create social-media-poster
)

echo.
echo ========================================
echo Skill directories created!
echo ========================================
echo.
echo Please run this script, then I'll create the SKILL.md files.
echo.
pause
