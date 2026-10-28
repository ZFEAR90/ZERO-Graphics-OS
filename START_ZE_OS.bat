@echo off
cd /d "%~dp0"
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    if not exist .venv\Scripts\python.exe py -3 -m venv .venv
) else (
    if not exist .venv\Scripts\python.exe python -m venv .venv
)
if not exist .venv\Scripts\python.exe goto failed
.venv\Scripts\python.exe -c "import requests, bs4, playwright" >nul 2>&1
if errorlevel 1 (
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 goto failed
)
.venv\Scripts\python.exe ze_local_importer.py --check-browser
if errorlevel 1 (
    echo Installing the browser needed to capture public posts...
    .venv\Scripts\python.exe -m playwright install chromium
    if errorlevel 1 (
        echo Browser installation failed. Metadata import may still work, but post screenshots need Chromium.
    )
)
.venv\Scripts\python.exe ze_local_importer.py
goto end
:failed
echo Setup failed. Install Python 3.10 or newer, then run this file again.
:end
pause
