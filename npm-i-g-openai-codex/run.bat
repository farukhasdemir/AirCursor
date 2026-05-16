@echo off
setlocal

set "PYTHON=C:\Users\oem\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
set "VENV_PYTHON=%~dp0.venv\Scripts\python.exe"

if not exist "%VENV_PYTHON%" (
    "%PYTHON%" -m venv "%~dp0.venv"
)

"%VENV_PYTHON%" -m pip install -r "%~dp0requirements.txt"
"%VENV_PYTHON%" "%~dp0hand_mouse.py"
