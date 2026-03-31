@echo off
REM Create Social_Queue directory structure

if not exist "AI_Employee_Vault\Social_Queue" mkdir "AI_Employee_Vault\Social_Queue"
if not exist "AI_Employee_Vault\Social_Queue\Posted" mkdir "AI_Employee_Vault\Social_Queue\Posted"
if not exist "AI_Employee_Vault\Social_Queue\Failed" mkdir "AI_Employee_Vault\Social_Queue\Failed"

echo Social_Queue directories created successfully!
