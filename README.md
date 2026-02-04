# Label Printer GUI

A cross-platform barcode label printing application with a modern GUI. Create, generate, and print labels with automatic Code128 barcode encoding.

## Features

✨ **Core Features**
- 🎨 Beautiful Kivy GUI interface
- 📊 Automatic Code128 barcode generation
- 📄 High-quality PDF label generation
- 💾 Automatic PDF backup system
- ✅ Input validation with 25-character limit
- 🔢 Number-only filter for quantity field

🖨️ **Printer Support**
- Windows printer detection and printing
- Linux CUPS printer support
- macOS printing support
- PDF fallback (works everywhere)

🚀 **Distribution**
- PyInstaller support for standalone Windows .exe
- No Python installation needed
- Cross-platform source code (Windows, Linux, macOS)

## Quick Start

### Option 1: Python Source (Recommended for Development)

```bash
# 1. Clone/Download the project
cd Label-design

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements_gui.txt

# 4. Run the app
python label_printer_gui.py
```

### Option 2: Windows Standalone Executable

1. Download `LabelPrinter.exe` from releases
2. Double-click to run (no Python needed!)
3. First run takes ~5 seconds to initialize

## Building Your Own Executable

### Windows Build Steps

```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Install PyInstaller
pip install pyinstaller

# 3. Build executable
python build_exe.py
```

Your executable will be in `dist/LabelPrinter.exe` (~200 MB)

### Manual Build Command

```bash
pyinstaller --onefile --windowed --name=LabelPrinter ^
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
  label_printer_gui.py
```

## File Structure

```
Label-design/
├── label_printer_gui.py          # Main GUI application
├── print_label.py                # Printing functionality
├── print_label_pdf.py            # PDF generation
├── build_exe.py                  # PyInstaller build script
├── requirements_gui.txt          # GUI dependencies
├── pdf_backup/                   # Generated label PDFs
├── dist/                         # Built executables
├── documentation/                # Docs and guides
│   ├── WINDOWS_SETUP.md
│   ├── PYINSTALLER_GUIDE.md
│   └── [other docs]
└── venv/                         # Python virtual environment
```

## Dependencies

**Required (Core):**
- `python-barcode` - Barcode generation
- `pillow` - Image processing
- `reportlab` - PDF generation

**GUI:**
- `kivy` - Cross-platform GUI framework

**Optional (Printing):**
- `pycups` - Linux CUPS support
- `pywin32` - Windows printer support

## Usage

### Basic Workflow

1. **Enter Data:**
   - **SAP-Nr**: Article code (up to 25 chars)
   - **Cantitate**: Quantity (numbers only)
   - **ID rola**: Reel/Cable ID (up to 25 chars)

2. **Select Printer:**
   - Choose from detected printers
   - Or select "PDF" for PDF output

3. **Print:**
   - Click "PRINT LABEL"
   - PDF is auto-saved to `pdf_backup/` folder
   - Label sent to printer

### PDF Backup

All generated labels are automatically saved with timestamps:
```
pdf_backup/
├── final_label_20260205_120530.pdf
├── final_label_20260205_120542.pdf
└── final_label_20260205_120555.pdf
```

## Guides

- **[WINDOWS_SETUP.md](documentation/WINDOWS_SETUP.md)** - Windows installation guide
- **[PYINSTALLER_GUIDE.md](documentation/PYINSTALLER_GUIDE.md)** - Building executables
- **[documentation/](documentation/)** - All documentation

## Troubleshooting

### "No Printers Found"
This is normal. Select "PDF" option - labels will be saved to `pdf_backup/` folder.

### "GUI Won't Start"
Ensure all dependencies are installed:
```bash
pip install -r requirements_gui.txt
```

### Windows Executable Issues
- Update PyInstaller: `pip install --upgrade pyinstaller`
- Rebuild: `python build_exe.py`
- Check dependencies: `pip list`

### Kivy Graphics Issues
On Linux, you may need SDL2 dependencies:
```bash
sudo apt-get install libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
```

## Platform Support

| Platform | Source | Executable | Status |
|----------|--------|-----------|--------|
| Windows | ✅ Yes | ✅ Yes | ✅ Fully Supported |
| Linux | ✅ Yes | ❌ No | ✅ Fully Supported |
| macOS | ✅ Yes | ⚠️ Possible | ⚠️ Untested |

## Technical Details

### Barcode Format
- **Type**: Code128
- **Max Length**: 25 characters
- **DPI**: 300 (print quality)

### PDF Specifications
- **Page Size**: 11.5 x 8 cm (landscape)
- **Quality**: High-resolution barcodes
- **Font**: Helvetica with automatic sizing

### GUI Specifications
- **Framework**: Kivy 2.3+
- **Size**: 420 x 700 pixels (mobile-optimized)
- **Color**: White text on dark background

## Contributing

Feel free to fork, modify, and improve!

Suggested improvements:
- [ ] Custom barcode formats (QR, Code39, etc.)
- [ ] Batch label printing
- [ ] Label preview before printing
- [ ] Printer-specific settings
- [ ] Multi-language support
- [ ] Database integration

## License

Open source - modify and use freely

## Support

For issues, questions, or suggestions:
1. Check the documentation in `documentation/` folder
2. Review the code comments
3. Test with the source code first before building exe

---

**Status**: Production Ready ✅

Last Updated: February 2026
