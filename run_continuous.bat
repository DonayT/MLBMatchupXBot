@echo off
echo ========================================
echo    MLB Matchup Bot - Continuous Run
echo ========================================
echo.

cd MLB_Matchup\scripts
powershell -ExecutionPolicy Bypass -File run_continuously.ps1

echo.
echo Continuous script completed!
pause 