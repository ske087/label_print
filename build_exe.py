"""
PyInstaller build script for Label Printer GUI
Run this to create a standalone Windows executable
"""

import os
import sys
from PyInstaller import __main__ as pyi_main

# Get the current directory
script_dir = os.path.dirname(os.path.abspath(__file__))

# PyInstaller arguments
args = [
    'label_printer_gui.py',
    '--onefile',  # Create a single executable
    '--windowed',  # Don't show console window
    '--name=LabelPrinter',  # Executable name
    '--distpath=./dist',  # Output directory
    '--buildpath=./build',  # Build directory
    '--hidden-import=kivy',
    '--hidden-import=kivy.core.window',
    '--hidden-import=kivy.core.text',
    '--hidden-import=kivy.core.image',
    '--hidden-import=kivy.uix.boxlayout',
    '--hidden-import=kivy.uix.gridlayout',
    '--hidden-import=kivy.uix.label',
    '--hidden-import=kivy.uix.textinput',
    '--hidden-import=kivy.uix.button',
    '--hidden-import=kivy.uix.spinner',
    '--hidden-import=kivy.uix.scrollview',
    '--hidden-import=kivy.uix.popup',
    '--hidden-import=kivy.clock',
    '--hidden-import=kivy.graphics',
    '--hidden-import=PIL',
    '--hidden-import=barcode',
    '--hidden-import=reportlab',
    '--hidden-import=print_label',
    '--hidden-import=print_label_pdf',
]

if __name__ == '__main__':
    print("=" * 60)
    print("Label Printer GUI - PyInstaller Build")
    print("=" * 60)
    print("\nBuilding standalone executable...")
    print("This may take a few minutes...\n")
    
    # Change to script directory
    os.chdir(script_dir)
    
    # Run PyInstaller
    pyi_main.run(args)
    
    print("\n" + "=" * 60)
    print("Build Complete!")
    print("=" * 60)
    print("\nExecutable location: ./dist/LabelPrinter.exe")
    print("\nYou can now:")
    print("1. Double-click LabelPrinter.exe to run")
    print("2. Share the exe with others")
    print("3. Create a shortcut on desktop")
    print("\nNote: First run may take a moment as Kivy initializes")
