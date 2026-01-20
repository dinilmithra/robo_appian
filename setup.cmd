@echo off
setlocal

REM Resolve repo root (folder of this cmd)
set "SCRIPT_DIR=%~dp0"
set "TARGET=%SCRIPT_DIR%scripts\setup.py"

if not exist "%TARGET%" (
    echo Cannot find scripts\setup.py next to this wrapper.
    exit /b 1
)

echo Delegating to %TARGET% ...
python "%TARGET%" %*
pause
endlocal