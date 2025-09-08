@echo off
setlocal
cd /d %~dp0

REM Create venv if missing
if not exist .venv (
  py -m venv .venv
)

REM Ensure pip
".venv\Scripts\python" -m ensurepip --upgrade >nul 2>&1
".venv\Scripts\python" -m pip install --upgrade pip setuptools wheel

REM Install deps if not present (idempotent)
".venv\Scripts\python" -m pip install -r requirements.txt

REM Run server
".venv\Scripts\python" product.py
endlocal

