@echo off
REM Life Assistant Bot Startup Script

REM Change to project directory
cd /d "%~dp0"

REM Activate conda environment and run bot
call conda activate life-assistant
if errorlevel 1 (
    echo Failed to activate conda environment
    pause
    exit /b 1
)

python bot.py
if errorlevel 1 (
    echo Bot exited with error
    pause
    exit /b 1
)
