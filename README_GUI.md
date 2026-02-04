# Label Printer GUI Application

A modern Kivy-based graphical interface for printing labels with barcodes, featuring real-time preview and printer selection.

## Features

✓ **Two-Column Layout**
  - Left: Data entry form with input fields
  - Right: Real-time label preview

✓ **Input Fields**
  - SAP-Nr. Articol (SAP Number/Article)
  - Cantitate (Quantity)
  - ID rola cablu (Cable Reel ID)

✓ **Live Preview**
  - Real-time preview of label as you type
  - Label size: 11.5 cm × 8 cm
  - Shows barcode and all entered information

✓ **Printer Management**
  - Dropdown to select from available system printers
  - Automatic detection of installed CUPS printers

✓ **Printing**
  - Direct printing to selected printer
  - Background printing with status notifications
  - Error handling and user feedback

## Installation

### Prerequisites
- Python 3.7 or higher
- CUPS (Common Unix Printing System) - usually pre-installed on Linux
- System printer configured and installed

### Setup Steps

1. **Install dependencies:**
```bash
pip install -r requirements_gui.txt
```

2. **Install Kivy garden dependencies** (if using matplotlib preview):
```bash
garden install matplotlib
```

3. **Ensure system printer is configured:**
```bash
# Check available printers
lpstat -p -d

# Or using CUPS web interface
# Open: http://localhost:631
```

## Usage

### Run the GUI Application

```bash
python label_printer_gui.py
```

### Operation

1. **Enter Label Data:**
   - Type the SAP Number in the first field
   - Enter the quantity (numbers only)
   - Enter the Cable Reel ID

2. **Monitor Preview:**
   - The preview updates automatically as you type
   - Shows combined barcode with all entered data

3. **Select Printer:**
   - Use the dropdown to select your target printer
   - Default is "PDF" if no other printers available

4. **Print:**
   - Click "PRINT LABEL" button
   - Wait for confirmation message
   - Label will print to selected printer

## Label Format

The label contains:
- **Row 1:** SAP Number | Quantity | Cable ID (combined in barcode)
- **Barcode:** Code128 format encoding the combined information
- **Size:** 11.5 cm width × 8 cm height
- **DPI:** 300 DPI for high-quality printing

## File Structure

```
/srv/Label-design/
├── print_label.py           # Core printing functions
├── label_printer_gui.py      # Kivy GUI application
├── requirements.txt          # Original dependencies
├── requirements_gui.txt      # GUI-specific dependencies
└── how_to.txt               # Original documentation
```

## Troubleshooting

### No printers detected
- Check CUPS service: `sudo systemctl status cups`
- List printers: `lpstat -p`
- Restart CUPS if needed: `sudo systemctl restart cups`

### Preview not updating
- Ensure all input fields are properly connected
- Check console for error messages
- Verify PIL/Pillow installation: `python -c "from PIL import Image; print('OK')"`

### Print fails
- Verify printer name is correct
- Check printer status: `lpstat -p -d`
- Test direct print: `echo "test" | lp -d printername`
- Ensure CUPS daemon is running

### Kivy window sizing issues
- The app defaults to 1600×900 window
- Can be resized freely after launch
- Modify `Window.size = (1600, 900)` in code to change default

## Code Integration

To integrate the printing function into other applications:

```python
from print_label import print_label_standalone

# Print a label
success = print_label_standalone(
    value="YOUR_TEXT",
    printer="printername", 
    preview=0  # 0=no preview, 1-3=3s preview, >3=5s preview
)
```

## Requirements

- **kivy**: GUI framework
- **python-barcode**: Barcode generation
- **pillow**: Image processing
- **pycups**: CUPS printer interface
- **matplotlib**: (Optional) For advanced visualization

## License

Based on the existing print_label.py printing framework.

## Notes

- All data is combined into a single barcode for easy scanning
- Labels are printed at 300 DPI for sharp quality
- Temporary files are cleaned up automatically
- Printing happens in background threads to prevent UI blocking

## Support

For issues or questions, check:
1. Console output for error messages
2. CUPS printer configuration
3. System printer availability
4. Required dependencies installation
