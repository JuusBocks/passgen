@echo off
setlocal enabledelayedexpansion

REM passgen - Password Generator Desktop App
cd /d "%~dp0"

REM Check if virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run setup.bat first
    pause
    exit /b 1
)

REM Prefer pythonw.exe to avoid flashing console; fallback to python.exe
set "PYW=.venv\Scripts\pythonw.exe"
set "PY=.venv\Scripts\python.exe"

REM Ensure logs directory exists for error logging from the app
if not exist "logs" mkdir "logs" >nul 2>nul

if exist "%PYW%" (
    start "" "%PYW%" main.py
) else (
    start "" "%PY%" main.py
)

REM Exit batch immediately to let app run
exit /b 0
