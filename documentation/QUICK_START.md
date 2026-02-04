# Quick Start Guide - PDF Label Printing System

## Installation & Setup

### 1. Activate Virtual Environment
```bash
cd /srv/Label-design
source venv/bin/activate
```

### 2. Install Dependencies (One-time)
```bash
pip install -r requirements_gui.txt
```

Or manually:
```bash
pip install python-barcode pillow pycups kivy reportlab
```

## Running the Application

### GUI Application (Recommended for Users)
```bash
source venv/bin/activate
python label_printer_gui.py
```

The GUI will open with:
- Input fields for SAP number, quantity, and lot ID
- Real-time label preview
- Printer selection dropdown
- Print button for easy printing

### Command Line (For Scripts/Integration)
```bash
source venv/bin/activate
python3 -c "from print_label import print_label_standalone; print_label_standalone('SAP-123|100|LOT-456', 'printer_name')"
```

## Using the System

### Basic PDF Label Generation
```python
from print_label import create_label_pdf

# Generate PDF file
pdf_file = create_label_pdf("SAP-123|100|LOT-456")
print(f"Created: {pdf_file}")
```

### Print to Printer
```python
from print_label import print_label_standalone

# PDF (recommended - highest quality)
print_label_standalone("SAP-123|100|LOT-456", "printer_name", use_pdf=True)

# PNG (fallback)
print_label_standalone("SAP-123|100|LOT-456", "printer_name", use_pdf=False)
```

### Advanced: Custom Label Size
```python
from print_label_pdf import PDFLabelGenerator

# Create 6cm × 4cm labels at 600 DPI
generator = PDFLabelGenerator(label_width=6, label_height=4, dpi=600)
pdf = generator.create_label_pdf(
    sap_nr="SAP-123",
    cantitate="100",
    lot_number="LOT-456",
    filename="custom_label.pdf"
)
```

## Key Features

### PDF Generation (Default)
- **Quality:** Professional vector-based format
- **File Size:** ~1.7 KB per label (91% smaller than PNG)
- **Scalability:** Works at any print resolution
- **Speed:** 200-500ms per label
- **Barcodes:** Sharp, reliable Code128 barcodes

### PNG Format (Fallback)
- **Quality:** Rasterized at 300 DPI
- **Compatibility:** Works with older systems
- **File Size:** ~19 KB per label
- **Use Case:** Legacy printer support

## Finding Printer Name

To see available printers:
```bash
# Using CUPS
lpstat -p -d

# Or in Python
import cups
conn = cups.Connection()
printers = conn.getPrinters()
for name in printers.keys():
    print(name)
```

## Generated Files

Labels are saved with timestamps:
- `final_label_20260205_000537.pdf` (timestamp format)
- Files are retained in current directory
- Easy to retrieve for reprinting

## Format Options

### Text Format: "SAP|QUANTITY|LOT"
```
"SAP-12345|100|LOT-ABC123"
     ↓        ↓     ↓
   SAP-Nr  Cantitate  Lot Nr
```

Each part becomes a barcode + label row in the output.

## Troubleshooting

### "No module named reportlab"
```bash
source venv/bin/activate
pip install reportlab
```

### "No such file or directory" (printer error)
This is normal - it means the printer doesn't exist.
Create a valid printer in CUPS first:
```bash
# Configure printer in CUPS web interface
http://localhost:631
```

### GUI Won't Start
Make sure display is available:
```bash
# Check if X11 is running
echo $DISPLAY
```

### Barcode Not Showing
The system falls back to text if barcode generation fails.
Make sure:
- Value is under 25 characters
- Text contains valid barcode characters
- System has write access to temp directory

## Testing

Run the comprehensive demo:
```bash
source venv/bin/activate
python demo_pdf_system.py
```

This tests:
- Basic PDF generation
- Custom dimensions
- Batch processing
- High DPI support
- PNG fallback
- API usage examples

## File Structure

```
/srv/Label-design/
├── label_printer_gui.py      # GUI Application
├── print_label.py            # Main printing module (updated with PDF support)
├── print_label_pdf.py        # PDF generation engine
├── demo_pdf_system.py        # Comprehensive demo
├── requirements.txt          # Base dependencies
├── requirements_gui.txt      # GUI dependencies
├── PDF_UPGRADE_GUIDE.md      # Full documentation
├── TEST_RESULTS_PDF_SYSTEM.md # Test results
├── QUICK_START.md            # This file
└── venv/                     # Virtual environment
```

## Performance

| Task | Time | Notes |
|------|------|-------|
| Single PDF generation | 200-500ms | Per label |
| Single PNG generation | 300-600ms | Legacy |
| Batch (4 labels) | ~1.5 seconds | PDF format |
| Print submission | ~100ms | To CUPS |

## Tips & Best Practices

1. **Use PDF by default** - Better quality, smaller files
2. **Keep PNG option** - For backward compatibility
3. **Use 300 DPI** - Standard for barcode scanning
4. **Archive PDFs** - Smaller file sizes = less storage
5. **Test printer** - Verify PDF support before large runs

## Support Resources

- **Full Documentation:** See `PDF_UPGRADE_GUIDE.md`
- **Test Results:** See `TEST_RESULTS_PDF_SYSTEM.md`
- **Demo Code:** Run `demo_pdf_system.py`
- **Code Examples:** Look at function docstrings

## Environment Variables

Optional environment customization:
```bash
# Set default printer
export CUPS_DEFAULT_PRINTER="your_printer_name"

# Set temp directory for label files
export TMPDIR="/path/to/temp"
```

---

**Status:** ✓ Production Ready  
**Last Updated:** February 5, 2026  
**Version:** 2.0 (PDF-based)
