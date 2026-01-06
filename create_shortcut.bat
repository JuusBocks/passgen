@echo off
REM Create Start Menu Shortcut for passgen (Password Generator)
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
set "SHORTCUT_NAME=passgen.lnk"
set "PYW=!SCRIPT_DIR!.venv\Scripts\pythonw.exe"
set "PY=!SCRIPT_DIR!.venv\Scripts\python.exe"

REM Choose pythonw.exe if available (no console window), otherwise python.exe
set "TARGET_PATH="
if exist "%PYW%" (
    set "TARGET_PATH=%PYW%"
) else (
    set "TARGET_PATH=%PY%"
)

REM Use PowerShell to create the shortcut
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
    "$WshShell = New-Object -ComObject WScript.Shell; " ^
    "$Shortcut = $WshShell.CreateShortcut('%START_MENU%\%SHORTCUT_NAME%'); " ^
    "$Shortcut.TargetPath = '%TARGET_PATH%'; " ^
    "$Shortcut.Arguments = 'main.py'; " ^
    "$Shortcut.WorkingDirectory = '%SCRIPT_DIR%'; " ^
    "$Shortcut.Description = 'Generate secure passwords with custom instructions'; " ^
    "$Shortcut.Save(); " ^
    "Write-Host 'Shortcut created successfully!'; " ^
    "Write-Host 'You can now find passgen in your Start Menu.'"

echo.
echo Setup complete! You can now search for "passgen" in Windows Start Menu.
pause
