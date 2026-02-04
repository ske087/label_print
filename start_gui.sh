#!/bin/bash

# Label Printer GUI - Quick Start Script
# This script sets up and runs the Label Printer GUI application

set -e

echo "=========================================="
echo "Label Printer GUI - Setup & Run"
echo "=========================================="
echo ""

# Check Python installation
echo "[1/4] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.7 or higher."
    exit 1
fi
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Check CUPS
echo "[2/4] Checking CUPS (printer service)..."
if ! command -v lpstat &> /dev/null; then
    echo "⚠ CUPS not found. Please install with: sudo apt-get install cups"
    echo "  Proceeding anyway - will use PDF printer"
else
    echo "✓ CUPS found"
    echo "  Available printers:"
    lpstat -p -d | head -5
fi
echo ""

# Install dependencies
echo "[3/4] Installing Python dependencies..."
if [ -f "requirements_gui.txt" ]; then
    pip install -r requirements_gui.txt
    echo "✓ Dependencies installed"
else
    echo "⚠ requirements_gui.txt not found"
    echo "  Installing Kivy and related packages manually..."
    pip install kivy python-barcode pillow pycups
fi
echo ""

# Run the application
echo "[4/4] Starting Label Printer GUI..."
echo "=========================================="
echo ""
python3 label_printer_gui.py

