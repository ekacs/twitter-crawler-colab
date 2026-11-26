@echo off
setlocal enabledelayedexpansion
title Twitter (X) Data Crawler Portable

cd /d "%~dp0"

echo ===================================================
echo     Twitter (X) Data Crawler - Portable Edition
echo ===================================================
echo.

set "PYTHON_EXE=%~dp0runtime\python\python.exe"
set "NODE_DIR=%~dp0runtime\node"
set "PLAYWRIGHT_BROWSERS_PATH=%~dp0runtime\playwright-browsers"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python portable tidak ditemukan di:
    echo "%PYTHON_EXE%"
    echo.
    echo Pastikan folder runtime sudah dibuat dengan menjalankan build_portable.bat!
    pause
    exit /b 1
)

:: Daftarkan node portabel ke PATH
if exist "%NODE_DIR%" (
    set "PATH=%NODE_DIR%;!PATH!"
)

echo [*] Menyiapkan aplikasi...
echo [*] Membuka Twitter Crawler di browser Anda...
echo [*] Jangan tutup jendela command prompt ini selama aplikasi digunakan.
echo.

"%PYTHON_EXE%" -m streamlit run app.py --server.headless=false --server.port=8501

pause
