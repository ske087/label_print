# Building LabelPrinter.exe on Windows

This guide explains how to build a standalone `LabelPrinter.exe` single-file executable on a Windows machine.

## Prerequisites

1. **Python 3.10 or higher** - Download from https://www.python.org/
   - ⚠️ **IMPORTANT**: Check "Add Python to PATH" during installation
   - Verify: Open Command Prompt and type `python --version`

2. **Git** (optional, for cloning the repository)

3. **Internet connection** - To download dependencies

## Quick Start (Using Provided Scripts)

### Option 1: Batch Script (Recommended for CMD users)

1. Open **Command Prompt** (cmd.exe)
2. Navigate to the project folder:
   ```
   cd C:\path\to\label_print
   ```
3. Run the build script:
   ```
   build_windows.bat
   ```
4. Wait 5-15 minutes for the build to complete
5. The executable will be in: `dist\LabelPrinter.exe`

### Option 2: PowerShell Script

1. Open **PowerShell** (as Administrator recommended)
2. Navigate to the project folder:
   ```
   cd C:\path\to\label_print
   ```
3. Allow script execution (if needed):
   ```
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
4. Run the build script:
   ```
   .\build_windows.ps1
   ```
5. Wait 5-15 minutes for the build to complete
6. The executable will be in: `dist\LabelPrinter.exe`

## Manual Build Steps

If you prefer to run commands manually:

### Step 1: Prepare Python Environment

```bash
# Upgrade pip, setuptools, and wheel
python -m pip install --upgrade pip setuptools wheel
```

### Step 2: Install Dependencies

```bash
# Install required Python packages
pip install python-barcode pillow reportlab kivy==2.2.1 pyinstaller==6.1.0
```

### Step 3: Build the Executable

```bash
# Create single-file executable
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
```

The build process will take 5-15 minutes depending on your PC speed.

### Step 4: Test the Executable

```bash
# Run the built executable
dist\LabelPrinter.exe
```

## Output

After successful build, you'll have:

```
dist/
└── LabelPrinter.exe          ← Single executable file
```

## Distributing the Executable

You can:
1. **Copy `LabelPrinter.exe`** to any Windows PC (no Python needed!)
2. **Share via USB** or file transfer
3. **Create an installer** using NSIS or InnoSetup (optional)
4. **Upload to GitHub Releases** for public distribution

## Troubleshooting

### Error: "Python is not recognized"
- Reinstall Python and check "Add Python to PATH"
- Restart Command Prompt after reinstalling Python

### Error: "pip command not found"
- Use `python -m pip` instead of `pip`

### Build takes too long (>30 minutes)
- **Normal for first build** - Kivy framework is large
- Subsequent builds will be faster due to caching
- Close other applications to free up RAM

### Error: "No module named 'kivy'"
- Make sure dependencies installed correctly: `pip install kivy==2.2.1`
- Check internet connection

### Error: "LabelPrinter.exe won't start"
- Make sure all files are in the project folder:
  - `label_printer_gui.py`
  - `print_label.py`
  - `print_label_pdf.py`
- Antivirus might be blocking it - check security software

## Build Time Reference

- **First build**: 10-15 minutes (downloading dependencies)
- **Subsequent builds**: 5-10 minutes (cached dependencies)

## Advanced Options

### Reduce Build Time
```bash
pyinstaller label_printer_gui.py --onefile --windowed --name=LabelPrinter -y
```

### Add Icon to Executable
```bash
pyinstaller label_printer_gui.py --onefile --windowed --name=LabelPrinter --icon=path\to\icon.ico -y
```

### Faster: Use --onedir (Directory) instead of --onefile
```bash
pyinstaller label_printer_gui.py --onedir --windowed --name=LabelPrinter -y
# Builds in ~3-5 minutes, but creates a folder instead of single file
```

## Support

If you encounter issues:
1. Check the error message carefully
2. Make sure Python 3.10+ is installed
3. Verify all dependencies: `pip list`
4. Check internet connection
5. Try again with a fresh Command Prompt window
