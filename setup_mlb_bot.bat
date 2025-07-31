@echo off
echo ========================================
echo    MLB Matchup Bot - Setup
echo ========================================
echo.
echo Installing required dependencies...
echo.

pip install -r requirements.txt

echo.
echo Setup complete! You can now run:
echo   - run_mlb_matchup.bat (for single run)
echo   - run_mlb_continuous.bat (for continuous monitoring)
echo.
pause 