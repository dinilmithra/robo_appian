@echo off
setlocal enabledelayedexpansion

python --version
call python -m venv ./.venv
call .\.venv\Scripts\activate

ENDLOCAL