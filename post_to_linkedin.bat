@echo off
echo ========================================
echo Quick LinkedIn Post Creator
echo ========================================
echo.
echo This will create a post file for LinkedIn
echo.

REM Get post content from user
set /p "content=Enter your post content: "

if "%content%"=="" (
    echo ERROR: No content entered!
    pause
    exit /b 1
)

REM Generate filename with timestamp
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set filename=linkedin_post_%datetime:~0,8%_%datetime:~8,6%.md

REM Create post file
echo --- > "AI_Employee_Vault\Social_Queue\%filename%"
echo platforms: linkedin >> "AI_Employee_Vault\Social_Queue\%filename%"
echo --- >> "AI_Employee_Vault\Social_Queue\%filename%"
echo. >> "AI_Employee_Vault\Social_Queue\%filename%"
echo %content% >> "AI_Employee_Vault\Social_Queue\%filename%"

echo.
echo ========================================
echo Post Created Successfully!
echo ========================================
echo.
echo File: AI_Employee_Vault\Social_Queue\%filename%
echo.
echo To post it:
echo   python social_poster.py
echo.
echo Or edit the file to add:
echo   - More content
echo   - Hashtags
echo   - Scheduled time
echo.
pause
