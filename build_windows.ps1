# Label Printer - Windows Build Script (Single File EXE)
# This script builds a standalone LabelPrinter.exe on Windows
# Requirements: Python 3.10+ installed and in PATH

Write-Host ""
Write-Host "========================================================"
Write-Host "  Label Printer - Windows Build Script"
Write-Host "  Creates: LabelPrinter.exe (Single File)"
Write-Host "========================================================"
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "Python not found"
    }
} catch {
    Write-Host "ERROR: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "[1/5] Checking Python installation..." -ForegroundColor Cyan
Write-Host $pythonVersion
Write-Host ""

Write-Host "[2/5] Upgrading pip, setuptools, and wheel..." -ForegroundColor Cyan
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to upgrade pip" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "[3/5] Installing dependencies..." -ForegroundColor Cyan
Write-Host "Installing: python-barcode, pillow, reportlab, kivy, pyinstaller..."
pip install python-barcode pillow reportlab kivy==2.2.1 pyinstaller==6.1.0
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to install dependencies" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}
Write-Host ""

Write-Host "[4/5] Cleaning old build artifacts..." -ForegroundColor Cyan
if (Test-Path "dist") { Remove-Item -Recurse -Force "dist" }
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
Remove-Item -Force "*.spec" -ErrorAction SilentlyContinue
Write-Host ""

Write-Host "[5/5] Building executable with PyInstaller..." -ForegroundColor Cyan
Write-Host "This may take 5-15 minutes, please wait..."
Write-Host ""

$pyinstallerArgs = @(
    "label_printer_gui.py",
    "--onefile",
    "--windowed",
    "--name=LabelPrinter",
    "--distpath=./dist",
    "--workpath=./build",
    "--hidden-import=kivy",
    "--hidden-import=PIL",
    "--hidden-import=barcode",
    "--hidden-import=reportlab",
    "--hidden-import=print_label",
    "--hidden-import=print_label_pdf",
    "-y"
)

pyinstaller @pyinstallerArgs
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "========================================================"
Write-Host "  BUILD SUCCESSFUL!" -ForegroundColor Green
Write-Host "========================================================"
Write-Host ""
Write-Host "Executable Location: dist\LabelPrinter.exe" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Navigate to the dist folder"
Write-Host "  2. Double-click LabelPrinter.exe to run"
Write-Host "  3. You can copy LabelPrinter.exe to other machines"
Write-Host ""
Write-Host "Note: First run may take a moment as Kivy initializes"
Write-Host ""
Read-Host "Press Enter to exit"
