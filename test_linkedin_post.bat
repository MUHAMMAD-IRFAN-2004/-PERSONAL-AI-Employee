@echo off
echo ================================================
echo LinkedIn Quick Test
echo ================================================
echo.
echo Step 1: Creating test post...
echo.

REM Create Social_Queue if not exists
if not exist "AI_Employee_Vault\Social_Queue" mkdir "AI_Employee_Vault\Social_Queue"

REM Create test post
(
echo ---
echo platforms: linkedin
echo ---
echo.
echo 🚀 Test Post from AI Employee
echo.
echo Ye mera pehla automated LinkedIn post hai!
echo.
echo #AI #Automation #Test
) > "AI_Employee_Vault\Social_Queue\test_linkedin.md"

echo ✓ Test post created: AI_Employee_Vault\Social_Queue\test_linkedin.md
echo.
echo ================================================
echo Step 2: Starting Social Poster...
echo ================================================
echo.
echo Browser khulega...
echo Pehli baar manual login karna padega!
echo.
timeout /t 3
python social_poster.py

pause
