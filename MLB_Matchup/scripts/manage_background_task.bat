@echo off
echo ========================================
echo    MLB Lineup Bot - Task Manager
echo ========================================
echo.

:menu
echo Choose an option:
echo.
echo 1. View current task status
echo 2. Start the task now
echo 3. Stop the task
echo 4. Delete the task
echo 5. Create new task
echo 6. Exit
echo.
set /p choice="Enter your choice (1-6): "

if "%choice%"=="1" goto view
if "%choice%"=="2" goto start
if "%choice%"=="3" goto stop
if "%choice%"=="4" goto delete
if "%choice%"=="5" goto create
if "%choice%"=="6" goto exit
echo Invalid choice. Please try again.
goto menu

:view
echo.
echo 📋 Current Task Status:
echo ========================================
schtasks /query /tn "MLB Lineup Bot" /fo table
echo.
pause
goto menu

:start
echo.
echo 🚀 Starting MLB Lineup Bot task...
schtasks /run /tn "MLB Lineup Bot"
if %errorLevel% == 0 (
    echo ✅ Task started successfully!
) else (
    echo ❌ Failed to start task
)
echo.
pause
goto menu

:stop
echo.
echo 🛑 Stopping MLB Lineup Bot task...
schtasks /end /tn "MLB Lineup Bot"
if %errorLevel% == 0 (
    echo ✅ Task stopped successfully!
) else (
    echo ❌ Failed to stop task
)
echo.
pause
goto menu

:delete
echo.
echo ⚠️  WARNING: This will delete the MLB Lineup Bot task!
echo Are you sure you want to continue?
set /p confirm="Type 'yes' to confirm: "
if not "%confirm%"=="yes" (
    echo Cancelled.
    goto menu
)

echo 🗑️  Deleting MLB Lineup Bot task...
schtasks /delete /tn "MLB Lineup Bot" /f
if %errorLevel% == 0 (
    echo ✅ Task deleted successfully!
) else (
    echo ❌ Failed to delete task
)
echo.
pause
goto menu

:create
echo.
echo 🔧 Creating new MLB Lineup Bot task...
echo This requires administrator privileges.
echo.
pause

REM Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo ✅ Running as administrator
) else (
    echo ❌ This requires administrator privileges
    echo Please right-click and "Run as administrator"
    pause
    goto menu
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
    goto menu
)

REM Get full path to Python
for /f "delims=" %%i in ('where python') do set "PYTHON_PATH=%%i"

echo Creating scheduled task...
schtasks /create /tn "MLB Lineup Bot" /tr "\"%PYTHON_PATH%\" \"%SCRIPT_DIR%..\src\MLBMatchup.py\"" /sc minute /mo 15 /f

if %errorLevel% == 0 (
    echo ✅ Task created successfully!
    echo.
    echo 📋 Task Details:
    echo    Name: "MLB Lineup Bot"
    echo    Runs: Every 15 minutes
    echo    Command: "%PYTHON_PATH%" "%SCRIPT_DIR%..\src\MLBMatchup.py"
) else (
    echo ❌ Failed to create task
    echo Error code: %errorLevel%
)

echo.
pause
goto menu

:exit
echo.
echo 👋 Goodbye!
pause
exit /b 0 