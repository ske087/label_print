#!/usr/bin/env python3
"""
Label Printer GUI - Setup and Launcher Script
Handles installation and execution of the Label Printer GUI application
"""

import subprocess
import sys
import os
import shutil

def check_python_version():
    """Check if Python version is 3.7 or higher"""
    version_info = sys.version_info
    if version_info.major < 3 or (version_info.major == 3 and version_info.minor < 7):
        print("❌ Python 3.7 or higher required")
        return False
    print(f"✓ Python {version_info.major}.{version_info.minor}.{version_info.micro} found")
    return True

def check_cups():
    """Check if CUPS is installed"""
    if shutil.which('lpstat'):
        print("✓ CUPS found")
        # Try to get printer list
        try:
            result = subprocess.run(['lpstat', '-p', '-d'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("  Available printers:")
                for line in result.stdout.strip().split('\n')[:5]:
                    if line:
                        print(f"    {line}")
            return True
        except:
            print("⚠ CUPS found but couldn't list printers")
            return True
    else:
        print("⚠ CUPS not found. Printer functionality may be limited.")
        print("  Install with: sudo apt-get install cups")
        return False

def install_dependencies():
    """Install required Python packages"""
    packages = [
        'kivy',
        'python-barcode',
        'pillow',
        'pycups'
    ]
    
    print("Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def run_gui():
    """Run the GUI application"""
    try:
        print("\nStarting Label Printer GUI...")
        print("=" * 50)
        subprocess.call([sys.executable, 'label_printer_gui.py'])
        return True
    except Exception as e:
        print(f"❌ Failed to run GUI: {e}")
        return False

def main():
    """Main setup and launcher"""
    print("=" * 50)
    print("Label Printer GUI - Setup & Launcher")
    print("=" * 50)
    print()
    
    # Step 1: Check Python
    print("[1/4] Checking Python installation...")
    if not check_python_version():
        sys.exit(1)
    print()
    
    # Step 2: Check CUPS
    print("[2/4] Checking printer service...")
    check_cups()
    print()
    
    # Step 3: Install dependencies
    print("[3/4] Installing dependencies...")
    if not install_dependencies():
        print("⚠ Some dependencies may not have installed")
        response = input("Continue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    print()
    
    # Step 4: Run application
    print("[4/4] Launching application...")
    run_gui()

if __name__ == '__main__':
    main()
