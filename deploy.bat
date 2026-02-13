@echo off
echo 🏎️ SmartCar AI-Dealer - Auto Deploy
echo =====================================

:: Ask for commit message
set /p MSG="Enter update description: "

:: Git commands
git add -A
git commit -m "%MSG%"
git push origin main

echo.
echo ✅ Successfully pushed to GitHub!
echo 🔗 https://github.com/Osamaamhmad67/SmartCar_AI_Dealer
pause
