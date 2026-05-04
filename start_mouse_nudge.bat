@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>&1
if %errorlevel%==0 (
    py -3 mouse_nudge.py
) else (
    python mouse_nudge.py
)
