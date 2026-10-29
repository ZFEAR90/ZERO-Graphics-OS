@echo off
setlocal
title Main roll - Beta 2.7.8
cd /d "%~dp0"
if not exist "ZE_OS_Mouwajaha_V07.html" (
    echo Main roll HTML is missing.
    echo Extract the entire ZIP to a folder, then run TEST_MAIN_ROLL.bat again.
    pause
    exit /b 1
)
echo Opening Main roll Beta 2.7.8 in your default browser...
echo This quick test does not need Python or an Internet connection.
echo For public-post URL import, run START_ZE_OS.bat instead.
start "" "%~dp0ZE_OS_Mouwajaha_V07.html"
if errorlevel 1 (
    echo Could not open the editor. Open ZE_OS_Mouwajaha_V07.html in Edge or Chrome.
    pause
    exit /b 1
)
endlocal
