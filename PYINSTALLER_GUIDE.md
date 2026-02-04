# Building a Standalone EXE with PyInstaller

This guide explains how to create a standalone Windows executable (`.exe`) file that doesn't require Python to be installed.

## Quick Start (Windows)

### Prerequisites
- Python 3.11+ installed
- Virtual environment activated
- All dependencies installed

### One-Command Build

```bash
# Activate virtual environment
venv\Scripts\activate

# Build the executable
python build_exe.py
```

That's it! Your executable will be in `dist/LabelPrinter.exe`

---

## What Happens During Build

1. **Analyzes your code** - Finds all imported modules
2. **Collects dependencies** - Bundles Kivy, PIL, barcode, reportlab, etc.
3. **Creates executable** - Packages everything into one `.exe` file
4. **Output**: `dist/LabelPrinter.exe` (~150-200 MB)

---

## Detailed Build Instructions

### Step 1: Install PyInstaller
```bash
venv\Scripts\activate
pip install pyinstaller
```

### Step 2: Build Using Script
```bash
python build_exe.py
```

### Step 3: Alternative Manual Build
If the script doesn't work, use this command directly:

```bash
pyinstaller ^
  --onefile ^
  --windowed ^
  --name=LabelPrinter ^
  --hidden-import=kivy ^
  --hidden-import=kivy.core.window ^
  --hidden-import=kivy.core.text ^
  --hidden-import=kivy.core.image ^
  --hidden-import=kivy.uix.boxlayout ^
  --hidden-import=kivy.uix.gridlayout ^
  --hidden-import=kivy.uix.label ^
  --hidden-import=kivy.uix.textinput ^
  --hidden-import=kivy.uix.button ^
  --hidden-import=kivy.uix.spinner ^
  --hidden-import=kivy.uix.scrollview ^
  --hidden-import=kivy.uix.popup ^
  --hidden-import=kivy.clock ^
  --hidden-import=kivy.graphics ^
  --hidden-import=PIL ^
  --hidden-import=barcode ^
  --hidden-import=reportlab ^
  --hidden-import=print_label ^
  --hidden-import=print_label_pdf ^
  --collect-all=kivy ^
  --collect-all=PIL ^
  label_printer_gui.py
```

---

## Output Files

After building, you'll have:

```
Label-design/
├── dist/
│   └── LabelPrinter.exe          ← Your standalone executable (150-200 MB)
├── build/                         ← Temporary build files (can delete)
└── label_printer.spec             ← PyInstaller spec file
```

---

## Running the Executable

### On Your Computer
1. Double-click `dist/LabelPrinter.exe`
2. App starts immediately (first run takes ~5 seconds)
3. Works like the Python version

### Sharing with Others
1. Copy `dist/LabelPrinter.exe` to a folder
2. Create a shortcut to it on the desktop
3. Share the folder or executable
4. **No Python installation needed on their computer!**

### Creating a Shortcut
1. Right-click `LabelPrinter.exe`
2. Send to → Desktop (create shortcut)
3. Double-click the shortcut to run

---

## Troubleshooting

### "Failed to build the executable"

**Solution 1**: Check Python version
```bash
python --version  # Should be 3.11+
```

**Solution 2**: Update PyInstaller
```bash
pip install --upgrade pyinstaller
```

**Solution 3**: Install missing dependencies
```bash
pip install -r requirements_windows.txt
pip install pyinstaller
```

### "DLL load failed" when running exe

This usually means a library isn't bundled correctly.

**Solution**: Rebuild with verbose output
```bash
pyinstaller --debug=imports label_printer_gui.py
```

### Executable is very large (200+ MB)

This is normal for Kivy applications. The size includes:
- Python runtime (~50 MB)
- Kivy framework (~30 MB)
- Dependencies (PIL, barcode, reportlab, etc.) (~20 MB)
- Your code (~1 KB)

You can reduce size slightly with:
```bash
--exclude-module=matplotlib
--exclude-module=numpy
--exclude-module=scipy
```

### Slow to start (5-10 seconds)

Normal for Kivy apps. The first startup initializes:
- Python runtime
- Kivy graphics system
- Font rendering
- Window initialization

Subsequent runs are faster (~3 seconds).

---

## Advanced Options

### Add an Icon
1. Create a 256x256 PNG icon: `app_icon.png`
2. Convert to ICO: Use an online tool or ImageMagick
3. Build with icon:
```bash
pyinstaller --icon=app_icon.ico label_printer_gui.py
```

### Two-File Distribution
Instead of `--onefile`, use separate files for faster startup:
```bash
pyinstaller label_printer_gui.py
```
Creates `dist/` folder with all files (faster to run, easier to debug).

### Console Output
To see error messages, remove `--windowed`:
```bash
pyinstaller --onefile --name=LabelPrinter label_printer_gui.py
```

---

## Build Options Reference

| Option | Purpose |
|--------|---------|
| `--onefile` | Single executable (recommended) |
| `--windowed` | No console window |
| `--icon=file.ico` | Custom icon |
| `--hidden-import=module` | Include module that's not imported directly |
| `--collect-all=module` | Include all module data |
| `--distpath=folder` | Output directory |
| `--name=AppName` | Executable name |

---

## Final Steps

1. **Test the executable**: Run `LabelPrinter.exe` and test all features
2. **Verify PDF backup**: Check `pdf_backup/` folder is created
3. **Test printing**: Print a label to ensure PDF output works
4. **Share**: Distribute the `.exe` file to users

---

## Questions?

- Check the error message in the console
- Try rebuilding with `python build_exe.py`
- Ensure all dependencies are installed: `pip install -r requirements_windows.txt`
- Check that Python 3.11+ is installed: `python --version`

Good luck! 🚀
