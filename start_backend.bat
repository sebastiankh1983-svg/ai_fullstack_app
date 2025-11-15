@echo off
echo =====================================
echo   MNIST Backend wird gestartet...
echo =====================================
echo.

cd /d %~dp0

REM Virtuelle Umgebung aktivieren
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    echo ✓ Virtuelle Umgebung aktiviert
) else (
    echo ✗ Virtuelle Umgebung nicht gefunden!
    echo   Erstelle eine mit: python -m venv .venv
    pause
    exit /b 1
)

echo.
echo Starte Flask Backend auf http://localhost:5000
echo.

python app.py

pause

