#!/usr/bin/env python3
"""
Label Printer GUI - Project Validation Script
Checks if the project is properly set up and ready to run
"""

import os
import sys
import subprocess

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        size = os.path.getsize(filepath)
        print(f"✅ {description:<40} ({size:,} bytes)")
        return True
    else:
        print(f"❌ {description:<40} MISSING!")
        return False

def check_python():
    """Check Python version"""
    version = sys.version_info
    version_str = f"{version.major}.{version.minor}.{version.micro}"
    
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python version {version_str:<30} OK")
        return True
    else:
        print(f"❌ Python version {version_str:<30} TOO OLD (need 3.7+)")
        return False

def check_module(module_name):
    """Check if a Python module is installed"""
    try:
        __import__(module_name)
        print(f"✅ {module_name:<40} installed")
        return True
    except ImportError:
        print(f"⚠  {module_name:<40} not installed (will install on first run)")
        return False

def check_cups():
    """Check if CUPS is available"""
    try:
        result = subprocess.run(['lpstat', '-p'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            printer_count = result.stdout.count('printer')
            print(f"✅ CUPS available ({printer_count} printer(s) configured)")
            return True
    except:
        pass
    print(f"⚠  CUPS not accessible (install with: sudo apt-get install cups)")
    return False

def main():
    print_header("Label Printer GUI - Project Validation")
    
    all_ok = True
    
    # Check required files
    print("📋 Checking Required Files:")
    print("-" * 60)
    
    files_to_check = [
        ("label_printer_gui.py", "Main GUI Application"),
        ("print_label.py", "Printing Engine"),
        ("setup_and_run.py", "Setup Script"),
        ("requirements_gui.txt", "GUI Dependencies"),
        ("requirements.txt", "Original Dependencies"),
    ]
    
    for filepath, description in files_to_check:
        if not check_file(filepath, description):
            all_ok = False
    
    # Check documentation
    print("\n📚 Checking Documentation:")
    print("-" * 60)
    
    docs_to_check = [
        ("GETTING_STARTED.md", "Quick Start Guide"),
        ("README_GUI.md", "Feature Documentation"),
        ("TECHNICAL_DOCS.md", "Technical Reference"),
        ("FILE_GUIDE.md", "File Reference Guide"),
        ("IMPLEMENTATION_SUMMARY.md", "Implementation Summary"),
    ]
    
    for filepath, description in docs_to_check:
        if not check_file(filepath, description):
            all_ok = False
    
    # Check Python version
    print("\n🐍 Checking Python Environment:")
    print("-" * 60)
    if not check_python():
        all_ok = False
    
    # Check optional modules
    print("\n📦 Checking Python Modules:")
    print("-" * 60)
    
    modules = [
        ('kivy', 'Kivy GUI Framework'),
        ('PIL', 'Pillow (Image Processing)'),
        ('barcode', 'Barcode Generation'),
        ('cups', 'CUPS Interface'),
    ]
    
    optional_found = False
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {description:<40} installed")
            optional_found = True
        except ImportError:
            print(f"⚠  {description:<40} not installed (will install on first run)")
    
    # Check CUPS
    print("\n🖨️  Checking Printer Service:")
    print("-" * 60)
    check_cups()
    
    # Summary
    print_header("Summary & Next Steps")
    
    if all_ok:
        print("✅ All required files are present!\n")
        print("🚀 Ready to run! Use one of these commands:\n")
        print("   Option 1 (Recommended):")
        print("   $ python3 setup_and_run.py\n")
        print("   Option 2 (Manual):")
        print("   $ pip install -r requirements_gui.txt")
        print("   $ python3 label_printer_gui.py\n")
        print("   Option 3 (Bash):")
        print("   $ chmod +x start_gui.sh")
        print("   $ ./start_gui.sh\n")
    else:
        print("⚠️  Some files might be missing or issues detected.\n")
        print("👉 First run setup_and_run.py to install everything:")
        print("   $ python3 setup_and_run.py\n")
    
    print("📖 For detailed help, read:")
    print("   • GETTING_STARTED.md - Quick start guide")
    print("   • README_GUI.md - Full documentation")
    print("   • FILE_GUIDE.md - File reference")
    print()
    
    return 0 if all_ok else 1

if __name__ == '__main__':
    sys.exit(main())
