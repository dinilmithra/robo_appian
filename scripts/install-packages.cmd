@echo off
setlocal enabledelayedexpansion

call ./.venv/Scripts/activate

call py -m pip install --upgrade pip
call pip3 --version

call pip3 install setuptools

pause

ENDLOCAL
