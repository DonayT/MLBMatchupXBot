@echo off
echo ========================================
echo    MLB Lineup Bot - Background Setup
echo ========================================
echo.

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as administrator
) else (
    echo ❌ This script requires administrator privileges
    echo Please right-click and "Run as administrator"
    pause
    exit /b 1
)

REM Get the current directory and Python executable
set "SCRIPT_DIR=%~dp0"
set "PYTHON_EXE=python.exe"

REM Try to find Python in PATH
where python >nul 2>&1
if %errorLevel% neq 0 (
    echo ❌ Python not found in PATH
    echo Please make sure Python is installed and in your PATH
    pause
    exit /b 1
)

REM Get full path to Python
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"

echo 📍 Script Directory: %SCRIPT_DIR%
echo 🐍 Python Path: %PYTHON_PATH%
echo 📄 MLB Script: %SCRIPT_DIR%..\src\MLBMatchup.py
echo.

REM Check if MLB script exists
if not exist "%SCRIPT_DIR%..\src\MLBMatchup.py" (
    echo ❌ MLBMatchup.py not found in src directory
    pause
    exit /b 1
)

echo Creating Windows Task Scheduler job...
echo.

REM Create the scheduled task with full paths
schtasks /create /tn "MLB Lineup Bot" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_DIR%..\src\MLBMatchup.py\"" /sc minute /mo 15 /f

if %errorLevel% == 0 (
    echo.
    echo ✅ Task created successfully!
    echo.
    echo 📋 Task Details:
    echo    Name: "MLB Lineup Bot"
    echo    Runs: Every 15 minutes
    echo    Command: "%PYTHON_PATH%" "%SCRIPT_DIR%..\src\MLBMatchup.py"
    echo.
    echo 🔧 Management Commands:
    echo    View task: schtasks /query /tn "MLB Lineup Bot"
    echo    Delete task: schtasks /delete /tn "MLB Lineup Bot" /f
    echo    Run now: schtasks /run /tn "MLB Lineup Bot"
    echo.
    echo 🎯 The bot will now run automatically every 15 minutes!
    echo.
) else (
    echo ❌ Failed to create task
    echo Error code: %errorLevel%
)

echo Press any key to exit...
pause >nul 