@echo off
title PixelStream Bot - VIRAL EDITION 🚀
color 0A
cls
echo ========================================================
echo   PIXELSTREAM BOT - SYSTEM ONLINE v6.0
echo ========================================================
echo.
echo  [+] Initializing Core Modules...
echo  [+] Optimizing Environment...
echo.
echo  Press any key to LAUNCH...
pause >nul
echo.
echo  [!] Executing main entry point...
:: Try to find a main runner
if exist main.py python main.py
if exist index.html start index.html
if exist app.py python app.py
echo.
pause