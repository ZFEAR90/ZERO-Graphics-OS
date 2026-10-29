@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Run START_ZE_OS.bat first to set up the Python environment.
    pause
    exit /b 1
)
.venv\Scripts\python.exe -m playwright install chromium
if errorlevel 1 (
    echo Capture browser installation failed. Check your Internet connection.
) else (
    echo Capture browser installed. Restart START_ZE_OS.bat.
)
pause
endlocal
