@echo off
setlocal
cd /d "%~dp0"

echo ===================================================
echo     BUILD TWITTER CRAWLER PORTABLE
echo ===================================================
echo.
echo Sedang mendownload Python embeddable, Node.js portable,
echo dan menginstal semua library ke folder runtime...
echo.

python build_portable.py

echo.
pause
