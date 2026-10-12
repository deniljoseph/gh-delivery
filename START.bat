@echo off
title Geometry Home Delivery Management System
color 0A
echo ============================================================
echo   Geometry Home Delivery Management System
echo ============================================================
echo.
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Install from python.org
    pause & exit /b 1
)
echo [1/2] Checking dependencies...
pip install -r requirements_local.txt --quiet --disable-pip-version-check
echo [2/2] Starting server...
echo.
echo  Application URL : http://localhost:5000
echo  Default Login   : admin / admin123
echo  Press Ctrl+C to stop
echo ============================================================
start /b cmd /c "timeout /t 2 >nul && start http://localhost:5000"
python app.py
pause
