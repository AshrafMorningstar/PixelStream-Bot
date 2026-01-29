@echo off
setlocal
title PixelStream Bot - v6.0 Viral Edition
color 0A

:: Viral Header
echo ========================================================
echo    PIXELSTREAM BOT v6.0 - @AshrafMorningstar
echo    "Turns your terminal into a cinema."
echo ========================================================
echo.

:: 1. Auto-Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.10+ from python.org
    pause
    exit /b
)

:: 2. Auto-Install Dependencies (Fast Check)
if not exist ".venv" (
    echo [Check] Verifying requirements...
    pip install -r requirements.txt >nul 2>&1
    if %errorlevel% neq 0 (
        echo [Install] Installing dependencies...
        pip install -r requirements.txt
    ) else (
        echo [OK] Dependencies ready.
    )
)

:: 3. Launch Universal Updater (Silent) to ensure headers are fresh
python universal_update.py >nul 2>&1

:: 4. Run Bot with Viral Demo
echo.
echo [Launch] Starting Engine...
echo.

:: Play the "Rick Roll" (Classic Viral Test) or similar high-engagement video
python main.py "https://youtube.com/shorts/AS4731IMdUA" --color --loop

pause
