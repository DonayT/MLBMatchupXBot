@echo off
echo ========================================
echo    MLB Lineup Bot - Continuous Runner
echo ========================================
echo.
echo 🚀 Starting MLB Lineup Bot...
echo ⏰ Will run every 15 minutes
echo 🛑 Press Ctrl+C to stop
echo.

cd /d "%~dp0..\src"
python MLBMatchup.py

echo.
echo ⏳ Waiting 15 minutes...
timeout /t 900 /nobreak >nul

goto :eof 