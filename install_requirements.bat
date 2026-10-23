@echo off
title Install Requirements - Soulseek FLAC Downloader
echo ===================================================
echo   Installing Dependencies for FLAC Downloader
echo ===================================================
echo.
python -m pip install -r requirements.txt
echo.
if %ERRORLEVEL% equ 0 (
    echo [OK] All dependencies installed successfully!
) else (
    echo [ERROR] Failed to install dependencies. Make sure Python is installed and added to PATH.
)
echo.
pause
