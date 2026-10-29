@echo off
setlocal
cd /d "%~dp0"
if not exist "ZE_OS_Mouwajaha_V07.html" (
    echo Extract the entire ZIP first. The editor HTML is missing.
    pause
    exit /b 1
)
echo Opening OFFLINE editor - manual photos and video only.
echo For URL import use START_ZE_OS.bat instead.
start "" "%~dp0ZE_OS_Mouwajaha_V07.html"
endlocal
