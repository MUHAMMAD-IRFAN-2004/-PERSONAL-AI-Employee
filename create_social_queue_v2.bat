@echo off
echo Creating Social_Queue directory structure...

if not exist "AI_Employee_Vault" (
    echo Creating AI_Employee_Vault...
    mkdir "AI_Employee_Vault"
)

if not exist "AI_Employee_Vault\Social_Queue" (
    mkdir "AI_Employee_Vault\Social_Queue"
    echo Created: Social_Queue
)

if not exist "AI_Employee_Vault\Social_Queue\Posted" (
    mkdir "AI_Employee_Vault\Social_Queue\Posted"
    echo Created: Social_Queue\Posted
)

if not exist "AI_Employee_Vault\Social_Queue\Failed" (
    mkdir "AI_Employee_Vault\Social_Queue\Failed"
    echo Created: Social_Queue\Failed
)

REM Create README in Social_Queue
echo # Social Media Queue > "AI_Employee_Vault\Social_Queue\README.md"
echo. >> "AI_Employee_Vault\Social_Queue\README.md"
echo Drop your social media posts here as .md files. >> "AI_Employee_Vault\Social_Queue\README.md"
echo. >> "AI_Employee_Vault\Social_Queue\README.md"
echo ## Post Format >> "AI_Employee_Vault\Social_Queue\README.md"
echo. >> "AI_Employee_Vault\Social_Queue\README.md"
echo ```markdown >> "AI_Employee_Vault\Social_Queue\README.md"
echo --- >> "AI_Employee_Vault\Social_Queue\README.md"
echo platforms: linkedin, twitter >> "AI_Employee_Vault\Social_Queue\README.md"
echo --- >> "AI_Employee_Vault\Social_Queue\README.md"
echo. >> "AI_Employee_Vault\Social_Queue\README.md"
echo Your post content here! >> "AI_Employee_Vault\Social_Queue\README.md"
echo ``` >> "AI_Employee_Vault\Social_Queue\README.md"
echo. >> "AI_Employee_Vault\Social_Queue\README.md"
echo After posting, files move to Posted/ or Failed/ >> "AI_Employee_Vault\Social_Queue\README.md"

echo.
echo ✓ All directories created successfully!
echo ✓ README.md created in Social_Queue
echo.
