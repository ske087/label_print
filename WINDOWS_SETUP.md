# Label Printer GUI - Windows Setup Guide

## Installation Steps

### 1. Install Python
- Download Python 3.11+ from [python.org](https://www.python.org/downloads/)
- **Important**: Check "Add Python to PATH" during installation

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements_windows.txt
```

### 4. Optional: Windows Printer Support (pywin32)
After installing requirements, run:
```bash
python -m pip install --upgrade pywin32
python Scripts/pywin32_postinstall.py -install
```

This enables native Windows printer detection.

## Running the App

### From Command Prompt
```bash
venv\Scripts\activate
python label_printer_gui.py
```

### Create Shortcut (Optional)
Create a batch file `run_app.bat`:
```batch
@echo off
call venv\Scripts\activate.bat
python label_printer_gui.py
pause
```

Then double-click the batch file to run the app.

## Features

✅ **Cross-Platform GUI** - Works on Windows, Linux, and macOS
✅ **Barcode Generation** - Automatic Code128 barcode creation
✅ **PDF Output** - High-quality PDF labels stored in `pdf_backup/` folder
✅ **Printer Support** - Automatic printer detection (Windows, Linux, macOS)
✅ **Input Validation** - 25-character limit with real-time validation
✅ **PDF Backup** - All generated labels automatically saved

## Printer Setup

### Windows
1. Go to Settings → Devices → Printers & Scanners
2. Add your label printer
3. Run the app - printer will be auto-detected
4. Select printer from dropdown

### Alternative (No Printer)
- Select "PDF" option
- Labels will be saved to `pdf_backup/` folder
- Open and print from any PDF viewer

## Troubleshooting

### "No Printers Found"
- This is normal - select "PDF" option
- You can print PDFs manually from the backup folder
- Or install your printer driver

### Windows Defender Warning
- Click "More info" → "Run anyway"
- This is safe - the app is open-source

### Missing Dependencies
```bash
pip install --upgrade pip
pip install -r requirements_windows.txt
```

### Port Already in Use
If you get an error about ports, restart your computer or:
```bash
python -m pip uninstall -y pywin32
python -m pip install pywin32
```

## File Structure

```
Label-design/
├── label_printer_gui.py      # Main GUI application
├── print_label.py            # Print functionality
├── print_label_pdf.py        # PDF generation
├── requirements_windows.txt  # Windows dependencies
├── pdf_backup/               # Stored PDF labels
├── venv/                     # Virtual environment
└── documentation/            # Documentation files
```

## Tips

- **Character Limit**: Each field supports up to 25 characters (barcode limit)
- **Quantity Field**: Only numbers allowed
- **PDF Backup**: All labels automatically saved with timestamp
- **Cross-Platform**: Same code runs on Windows, Linux, and macOS

For more information, see the documentation folder.
