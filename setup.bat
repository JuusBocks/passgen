@echo off
REM Complete setup for passgen - Run this once
echo ========================================
echo passgen - Password Generator Setup
echo ========================================
echo.

REM Check if .venv exists
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

echo.
echo Installing dependencies...
".\.venv\Scripts\python.exe" -m pip install --upgrade pip -q
".\.venv\Scripts\python.exe" -m pip install --upgrade -r requirements.txt -q

echo.
echo Creating Start Menu shortcut...
call create_shortcut.bat

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo You can now:
echo 1. Search for "passgen" in Windows Start Menu
echo 2. Or run: run.bat
echo.
echo For more info, see QUICK_START.md or README.md
echo.
pause
