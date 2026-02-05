@echo off
REM Label Printer - Windows Build Script (Single File EXE)
REM This script builds a standalone LabelPrinter.exe on Windows
REM Requirements: Python 3.10-3.13 installed and in PATH
REM Note: Python 3.14+ may have compatibility issues

setlocal enabledelayedexpansion

echo.
echo ========================================================
echo   Label Printer - Windows Build Script
echo   Creates: LabelPrinter.exe (Single File)
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.10-3.13 from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/5] Checking Python installation...
python --version
echo.

REM Upgrade pip
echo [2/5] Upgrading pip, setuptools, and wheel...
python -m pip install --upgrade pip setuptools wheel
if errorlevel 1 (
    echo ERROR: Failed to upgrade pip
    pause
    exit /b 1
)
echo.

REM Install dependencies
echo [3/5] Installing dependencies...
echo Installing: python-barcode, pillow, reportlab, kivy, pyinstaller...
pip install python-barcode pillow reportlab kivy==2.2.1 pyinstaller==6.1.0
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo.

REM Clean old build
echo [4/5] Cleaning old build artifacts...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build
if exist "*.spec" del *.spec
echo.

REM Build with PyInstaller
echo [5/5] Building executable with PyInstaller...
echo This may take 5-15 minutes, please wait...
echo.

pyinstaller label_printer_gui.py ^
    --onefile ^
    --windowed ^
    --name=LabelPrinter ^
    --distpath=./dist ^
    --workpath=./build ^
    --hidden-import=kivy ^
    --hidden-import=PIL ^
    --hidden-import=barcode ^
    --hidden-import=reportlab ^
    --hidden-import=print_label ^
    --hidden-import=print_label_pdf ^
    -y

if errorlevel 1 (
    echo.
    echo ERROR: Build failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo ========================================================
echo   BUILD SUCCESSFUL!
echo ========================================================
echo.
echo Executable Location: dist\LabelPrinter.exe
echo.
echo Next steps:
echo   1. Navigate to the dist folder
echo   2. Double-click LabelPrinter.exe to run
echo   3. You can copy LabelPrinter.exe to other machines
echo.
echo Note: First run may take a moment as Kivy initializes
echo.
pause
