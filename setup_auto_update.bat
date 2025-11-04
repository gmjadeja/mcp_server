@echo off
REM Windows batch script to set up scheduled auto-updates
REM Run this script as Administrator to set up a scheduled task

echo Setting up scheduled auto-update task...

REM Get the current directory
set PROJECT_DIR=%~dp0
set PYTHON_PATH=%PROJECT_DIR%venv\Scripts\python.exe
set MANAGE_PATH=%PROJECT_DIR%manage.py

REM Create scheduled task to run weekly on Sundays at 2 AM
schtasks /create /tn "MCP Education Auto Update" /tr "\"%PYTHON_PATH%\" \"%MANAGE_PATH%\" update_content --all --days 7" /sc weekly /d SUN /st 02:00 /ru SYSTEM

echo.
echo Scheduled task created successfully!
echo Task name: MCP Education Auto Update
echo Schedule: Weekly on Sundays at 2:00 AM
echo Command: python manage.py update_content --all --days 7
echo.
echo To view the task: schtasks /query /tn "MCP Education Auto Update"
echo To delete the task: schtasks /delete /tn "MCP Education Auto Update" /f
pause

