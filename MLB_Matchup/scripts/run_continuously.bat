@echo off
echo ========================================
echo    MLB Lineup Bot - Continuous Runner
echo ========================================
echo.
echo 🚀 Starting MLB Lineup Bot...
echo ⏰ Will run every 15 minutes
echo 🛑 Press Ctrl+C to stop
echo.

:loop
echo.
echo 🕐 [%date% %time%] Running MLB script...
python ..\src\MLBMatchup.py
echo.
echo ⏳ Waiting 15 minutes until next run...
echo (Press Ctrl+C to stop)
timeout /t 900 /nobreak >nul
goto loop 