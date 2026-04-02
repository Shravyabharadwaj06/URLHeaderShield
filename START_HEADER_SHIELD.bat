@echo off
title Header Shield - Backend Server
color 0B
echo.
echo  ============================================
echo   HEADER SHIELD - Starting Security Backend
echo  ============================================
echo.

cd /d "%~dp0"
echo  Opening Header Shield in your default browser...
start Page1.html

cd headerback
echo  Activating virtual environment (if any)...
if exist "..\venv\Scripts\activate.bat" (
    call ..\venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
)
echo.
echo  Starting Django server on http://127.0.0.1:8000
echo  ======================================================
echo  Keep this window open while using Header Shield!
echo  If you close this window, the analysis will fail.
echo  Press Ctrl+C to stop the server when you are done.
echo  ======================================================
echo.
python manage.py runserver
pause
