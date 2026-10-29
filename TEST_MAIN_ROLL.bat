@echo off
setlocal
cd /d "%~dp0"
if not exist "START_ZE_OS.bat" (
    echo Extract the entire ZIP first. START_ZE_OS.bat is missing.
    pause
    exit /b 1
)
call "%~dp0START_ZE_OS.bat"
endlocal
