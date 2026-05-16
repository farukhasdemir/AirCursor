$ErrorActionPreference = "Stop"

$Python = "C:\Users\oem\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe"
$VenvPython = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (!(Test-Path $VenvPython)) {
    & $Python -m venv (Join-Path $PSScriptRoot ".venv")
}

& $VenvPython -m pip install -r (Join-Path $PSScriptRoot "requirements.txt")
& $VenvPython (Join-Path $PSScriptRoot "hand_mouse.py")
