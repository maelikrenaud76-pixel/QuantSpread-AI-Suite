@echo off
title QuantSpread AI Suite — Master Launcher
color 0A

:: ============================================================================
:: CONFIG
:: ============================================================================
set PY=py -3.10
set FOLDER=C:\Users\maeli\Documents\LSTM Trading

:: ============================================================================
:: HEADER
:: ============================================================================
cls
echo.
echo ============================================================
echo          QUANTSPREAD AI SUITE — MASTER LAUNCHER           
echo ============================================================
echo.
echo  Dossier : %FOLDER%
echo  Python  : 3.10 (TensorFlow 2.20 compatible)
echo ============================================================
echo.

:: ============================================================================
:: CHECK PYTHON
:: ============================================================================
%PY% --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERREUR] Python 3.10 n'est pas installe.
    echo Installe Python 3.10.12 pour utiliser TensorFlow 2.20.
    pause
    exit /b
)
echo [OK] Python 3.10 detecte.
echo.

:: ============================================================================
:: INSTALL DEPENDENCIES
:: ============================================================================
echo Voulez-vous verifier/installer les dependances ? (O/N)
set /p depChoice="> "

if /I "%depChoice%"=="O" (
    echo.
    echo [INSTALLATION] Mise a jour de pip...
    %PY% -m pip install --upgrade pip

    echo.
    echo [INSTALLATION] Installation/verification des modules...
    %PY% -m pip install yfinance numpy pandas matplotlib scikit-learn tensorflow==2.20 streamlit reportlab
    echo.
)

:: ============================================================================
:: MENU
:: ============================================================================
:menu
cls
echo ============================================================
echo          QUANTSPREAD AI SUITE — MENU PRINCIPAL
echo ============================================================
echo.
echo  1. Lancer QuantSpread AI Suite (principal)
echo  2. Lancer LSTMMiniSuite
echo  3. Lancer QuantReportGenerator
echo  4. Lancer QuantScanner
echo  5. Lancer QuantLiveMonitor
echo ------------------------------------------------------------
echo  0. Quitter
echo ============================================================
echo.
set /p choice="Votre choix : "

if "%choice%"=="1" goto launch_main
if "%choice%"=="2" goto launch_mini
if "%choice%"=="3" goto launch_report
if "%choice%"=="4" goto launch_scanner
if "%choice%"=="5" goto launch_live
if "%choice%"=="0" exit
goto menu

:: ============================================================================
:: LAUNCHERS
:: ============================================================================
:launch_main
cls
echo Lancement de QuantSpread_AI_Suite.py...
%PY% "%FOLDER%\QuantSpread_AI_Suite.py"
pause
goto menu

:launch_mini
cls
echo Lancement de LSTMMiniSuite.py...
%PY% "%FOLDER%\LSTMMiniSuite.py"
pause
goto menu

:launch_report
cls
echo Lancement de QuantReportGenerator.py...
%PY% "%FOLDER%\QuantReportGenerator.py"
pause
goto menu

:launch_scanner
cls
echo Lancement de QuantScanner.py...
%PY% "%FOLDER%\QuantScanner.py"
pause
goto menu

:launch_live
cls
echo Lancement de QuantLiveMonitor.py...
%PY% "%FOLDER%\QuantLiveMonitor.py"
pause
goto menu
