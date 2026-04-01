@echo off
REM LinkedIn Only - Twitter Automatic Nahi Khulega

echo ========================================
echo LinkedIn Only Post Creator
echo Twitter automatic NAHI khulega
echo ========================================
echo.

REM Generate filename with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set filename=linkedin_only_%datetime:~0,8%_%datetime:~8,6%.md

echo Aapka LinkedIn post content:
echo (Type karein aur Enter press karein)
echo.
set /p "content="

if "%content%"=="" (
    echo.
    echo ERROR: Content khali hai!
    pause
    exit /b 1
)

REM Create post file - SIRF LINKEDIN
echo --- > "AI_Employee_Vault\Social_Queue\%filename%"
echo platforms: linkedin >> "AI_Employee_Vault\Social_Queue\%filename%"
echo --- >> "AI_Employee_Vault\Social_Queue\%filename%"
echo. >> "AI_Employee_Vault\Social_Queue\%filename%"
echo %content% >> "AI_Employee_Vault\Social_Queue\%filename%"

echo.
echo ========================================
echo ✓ LinkedIn Post Banai Gayi!
echo ========================================
echo.
echo File: %filename%
echo Platform: SIRF LINKEDIN (Twitter nahi!)
echo.
echo Ab run karo:
echo   python social_poster.py
echo.
echo NOTE: Sirf LinkedIn browser khulega
echo       Twitter/x.com NAHI khulega!
echo.
pause
