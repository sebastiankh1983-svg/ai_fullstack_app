@echo off
setlocal EnableDelayedExpansion EnableExtensions
:: Neuaufbau der virtuellen Umgebung für das Backend (robust gegen WinError 5)

set QUICK=%1

echo ==============================================
echo  REBUILD VENV (MNIST BACKEND - ROBUST)
echo ==============================================

echo Beende evtl. laufende Python Prozesse...
taskkill /IM python.exe /F >nul 2>&1
taskkill /IM pythonw.exe /F >nul 2>&1

cd /d "%~dp0"

set "TARGET_ENV=.venv"
set "FALLBACK_ENV=.venv_new"

if exist "%TARGET_ENV%" (
  echo Entferne alte Umgebung...
  attrib -R -S -H "%TARGET_ENV%" /S /D >nul 2>&1
  rd /s /q "%TARGET_ENV%" >nul 2>&1
)

if exist "%TARGET_ENV%" (
  echo Ordner gesperrt - umbenennen...
  if exist "%TARGET_ENV%_old" rd /s /q "%TARGET_ENV%_old" >nul 2>&1
  ren "%TARGET_ENV%" "%TARGET_ENV%_old" >nul 2>&1
)

if exist "%TARGET_ENV%" (
  echo Fehler: Alte Umgebung konnte nicht entfernt werden.
  echo Bitte IDE/Explorer schliessen und erneut versuchen.
  pause
  exit /b 1
)

if /I "%QUICK%"=="quick" (
  echo QUICK-Modus abgeschlossen.
  goto :eof
)

echo Erstelle neue virtuelle Umgebung...
python -m venv "%TARGET_ENV%"

if not exist "%TARGET_ENV%\Scripts\activate.bat" (
  echo Fehler beim Erstellen der venv.
  pause
  exit /b 1
)

echo Aktiviere Umgebung...
call "%TARGET_ENV%\Scripts\activate.bat"

if errorlevel 1 (
  echo Fehler beim Aktivieren.
  pause
  exit /b 1
)

echo Aktualisiere pip...
python -m pip install --upgrade pip

if not exist "requirements.txt" (
  echo requirements.txt nicht gefunden.
  pause
  exit /b 1
)

echo Installiere Abhängigkeiten...
pip install -r requirements.txt

if errorlevel 1 (
  echo Fehler bei Installation. Versuche Force-Reinstall...
  pip install --no-cache-dir --force-reinstall -r requirements.txt
)

echo.
echo ==============================================
echo  Venv erfolgreich neu aufgebaut: %TARGET_ENV%
echo ==============================================
echo.
echo Starten Sie nun das Training:
echo   python NN_Model.py --model-type cnn --epochs 15 --batch 256
echo.
pause
goto :eof

