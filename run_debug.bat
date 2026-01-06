@echo off
setlocal enabledelayedexpansion

REM passgen - Debug launcher (shows console output and errors)
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

if not exist "logs" mkdir "logs" >nul 2>nul

echo Launching in debug mode...
".\.venv\Scripts\python.exe" main.py

echo.
echo (If the app did not open, check logs\passgen_error.log for details.)
pause


