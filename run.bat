@echo off
title Guide Book Generator - CBSE Class 9 and 10

REM Change to the directory where the batch file is located
cd /d "%~dp0"

echo ========================================
echo   Guide Book Generator
echo   CBSE Class 9 and 10 Study Guides
echo ========================================
echo.
echo Starting application...
echo.

REM Use port 8505 to avoid conflicts
C:\Python314\python.exe -m streamlit run app.py --server.port 8505

pause
