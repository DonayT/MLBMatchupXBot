@echo off
echo ========================================
echo    MLB Lineup Bot - Task Manager
echo ========================================
echo.

:menu
echo Choose an option:
echo 1. Check task status
echo 2. Run task now
echo 3. Stop task (disable)
echo 4. Start task (enable)
echo 5. Delete task completely
echo 6. View recent task history
echo 7. Exit
echo.2

set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto check_status
if "%choice%"=="2" goto run_now
if "%choice%"=="3" goto stop_task
if "%choice%"=="4" goto start_task
if "%choice%"=="5" goto delete_task
if "%choice%"=="6" goto view_history
if "%choice%"=="7" goto exit
echo Invalid choice. Please try again.
echo.
goto menu

:check_status
echo.
echo 📋 Checking task status...
schtasks /query /tn "MLB Lineup Bot" /fo table
echo.
pause
goto menu

:run_now
echo.
echo 🚀 Running task now...
schtasks /run /tn "MLB Lineup Bot"
if %errorLevel% == 0 (
    echo ✅ Task started successfully
) else (
    echo ❌ Failed to start task
)
echo.
pause
goto menu

:stop_task
echo.
echo ⏸️ Stopping task...
schtasks /change /tn "MLB Lineup Bot" /disable
if %errorLevel% == 0 (
    echo ✅ Task disabled successfully
) else (
    echo ❌ Failed to disable task
)
echo.
pause
goto menu

:start_task
echo.
echo ▶️ Starting task...
schtasks /change /tn "MLB Lineup Bot" /enable
if %errorLevel% == 0 (
    echo ✅ Task enabled successfully
) else (
    echo ❌ Failed to enable task
)
echo.
pause
goto menu

:delete_task
echo.
echo ⚠️ WARNING: This will permanently delete the task!
set /p confirm="Are you sure? (y/N): "
if /i "%confirm%"=="y" (
    echo 🗑️ Deleting task...
    schtasks /delete /tn "MLB Lineup Bot" /f
    if %errorLevel% == 0 (
        echo ✅ Task deleted successfully
    ) else (
        echo ❌ Failed to delete task
    )
) else (
    echo ❌ Deletion cancelled
)
echo.
pause
goto menu

:view_history
echo.
echo 📊 Recent task history (last 10 entries):
echo.
schtasks /query /tn "MLB Lineup Bot" /fo list | findstr /i "last"
echo.
pause
goto menu

:exit
echo.
echo �� Goodbye!
exit /b 0 