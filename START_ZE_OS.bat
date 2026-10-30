@echo off
setlocal
cd /d "%~dp0"
title Main roll - URL importer
if not exist "ZE_OS_Mouwajaha_V07.html" goto missing
if not exist "ze_local_importer.py" goto missing
if not exist "requirements.txt" goto missing
echo Main roll URL importer setup > STARTUP_LOG.txt
if exist ".venv\Scripts\python.exe" goto dependencies
py -3 -c "import sys;sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if not errorlevel 1 goto use_py
python -c "import sys;sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>&1
if errorlevel 1 goto python_missing
python -m venv .venv >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto failed
goto dependencies
:use_py
py -3 -m venv .venv >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto failed
:dependencies
echo Main roll URL importer - first setup may take a few minutes.
echo Setup details are saved in STARTUP_LOG.txt.
.venv\Scripts\python.exe -c "import sys;sys.exit(0 if sys.version_info >= (3,10) else 1)" >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto failed
.venv\Scripts\python.exe -c "import requests, bs4, playwright" >> STARTUP_LOG.txt 2>&1
if not errorlevel 1 goto ready
echo Installing URL import dependencies...
.venv\Scripts\python.exe -m pip --version >> STARTUP_LOG.txt 2>&1
if not errorlevel 1 goto install_dependencies
echo Repairing missing pip in the local Python environment...
.venv\Scripts\python.exe -m ensurepip --upgrade >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto pip_missing
.venv\Scripts\python.exe -m pip --version >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto pip_missing
:install_dependencies
.venv\Scripts\python.exe -m pip install -r requirements.txt >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto failed
.venv\Scripts\python.exe -c "import requests, bs4, playwright" >> STARTUP_LOG.txt 2>&1
if errorlevel 1 goto failed
:ready
echo Starting the connected editor. Keep this window open.
echo Public platforms may still require a manual upload if anonymous access is denied.
echo If screenshots are unavailable, run INSTALL_CAPTURE_BROWSER.bat separately.
.venv\Scripts\python.exe -u ze_local_importer.py --startup-log STARTUP_LOG.txt
if errorlevel 1 goto failed
goto end
:pip_missing
echo Python could not restore pip. The importer is NOT running.
if exist STARTUP_LOG.txt type STARTUP_LOG.txt
echo Open the official Python installer, choose Modify or Repair, and enable pip.
echo Then run START_ZE_OS.bat again. Your project files have not been removed.
echo To edit with local media now, run OFFLINE_MAIN_ROLL.bat.
goto end
:python_missing
echo Python 3.10 or newer is needed for URL importing.
echo Install Python from https://www.python.org/downloads/windows/ and enable its launcher.
echo To test without URL importing, run OFFLINE_MAIN_ROLL.bat.
goto end
:missing
echo Required files are missing. Extract the ENTIRE ZIP first.
goto end
:failed
echo Startup failed. The importer is NOT running.
if exist STARTUP_LOG.txt type STARTUP_LOG.txt
echo Keep this message or send STARTUP_LOG.txt for diagnosis.
:end
pause
endlocal
