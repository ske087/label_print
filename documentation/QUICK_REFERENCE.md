# Label Printing System - Quick Reference Card

## System Specifications ✓

| Parameter | Value | Notes |
|-----------|-------|-------|
| **Label Width** | 11.5 cm | Full width |
| **Label Height** | 8 cm | Full height |
| **Rows** | 3 | SAP-Nr, Cantitate, Lot Nr |
| **Barcode Height** | 18 mm (1.8 cm) | Fixed, optimal for scanning |
| **Barcode Format** | Code128 | Standard barcode format |
| **Character Limit** | 25 chars max | Per field |
| **DPI** | 300 | Print-ready quality |
| **File Format** | PDF | Vector-based, professional |
| **Margin** | 3 mm | All sides |

## Quick Start

### 1. Activate Environment
```bash
cd /srv/Label-design
source venv/bin/activate
```

### 2. Run GUI
```bash
python label_printer_gui.py
```

### 3. Enter Data
- SAP-Nr: Up to 25 characters
- Cantitate: Up to 25 characters
- Lot Nr: Up to 25 characters
- Select Printer

### 4. Print
- Click "PRINT LABEL"
- PDF generates automatically
- Sends to printer

## Command Line Usage

```bash
# Generate PDF label
python3 -c "from print_label import print_label_standalone; \
print_label_standalone('SAP-123|100|LOT-ABC', 'printer_name')"

# Generate without printing (test)
python3 -c "from print_label import create_label_pdf; \
pdf = create_label_pdf('SAP-123|100|LOT-ABC'); \
print(f'Generated: {pdf}')"
```

## Label Data Format

```
Input Format: "SAP|CANTITATE|LOT"

Example: "SAP-12345|100|LOT-ABC"
         └─────┬─────┘ └──┬──┘ └──┬──┘
         SAP-Nr   Qty    Lot Nr
         
Each becomes a barcode row in the PDF
```

## Barcode Specifications

| Aspect | Specification | Details |
|--------|---------------|---------|
| **Type** | Code128 | Standard barcode |
| **Height** | 18 mm | Fixed (1.8 cm) |
| **Width** | Auto | Fits within label |
| **Module Width** | 0.5 mm | Bar thickness |
| **Quiet Zone** | 2 mm | Auto-applied |
| **Max Length** | 25 chars | Auto-truncates |

## File Locations

```
/srv/Label-design/
├── label_printer_gui.py      ← GUI application
├── print_label.py            ← Main module (PDF/PNG)
├── print_label_pdf.py        ← PDF generation engine
├── requirements_gui.txt      ← Dependencies
└── venv/                     ← Virtual environment
```

## Generated Files

Labels are saved with timestamps:
```
final_label_20260205_001617.pdf
           └─────────┬─────────┘
           YYYYMMDD_HHMMSS
```

Files are retained in working directory for reprinting.

## Troubleshooting

### PDF Won't Generate
```bash
# Check dependencies
pip list | grep reportlab

# Reinstall if needed
pip install reportlab
```

### Barcode Won't Scan
- Verify printer DPI (300+ required)
- Check label dimensions (11.5cm × 8cm)
- Use "Borderless" printing
- Test with standard scanner

### Text Gets Cut Off
- Max 25 characters per field
- Longer text auto-truncates
- Check for special characters

### File Not Found
```bash
# Verify virtual environment is active
which python
# Should show: /srv/Label-design/venv/bin/python
```

## Printer Setup (CUPS)

### View Available Printers
```bash
lpstat -p -d
```

### Configure Printer Size
```bash
# Open CUPS web interface
http://localhost:631
```

### Test Print
```bash
python3 -c "from print_label import print_label_standalone; \
print_label_standalone('TEST|123|ABC', 'your_printer_name', use_pdf=True)"
```

## Documentation

- **Full Guide:** `PDF_UPGRADE_GUIDE.md`
- **Setup Guide:** `QUICK_START.md`
- **Barcode Details:** `BARCODE_HEIGHT_CORRECTION.md`
- **Test Results:** `TEST_RESULTS_PDF_SYSTEM.md`

## API Summary

### Simple Function
```python
from print_label import print_label_standalone
print_label_standalone(text, printer, use_pdf=True)
```

### PDF Generation
```python
from print_label import create_label_pdf
pdf_file = create_label_pdf("SAP|QTY|LOT")
```

### Advanced (Custom Size)
```python
from print_label_pdf import PDFLabelGenerator
gen = PDFLabelGenerator(label_width=11.5, label_height=8)
pdf = gen.create_label_pdf("SAP", "QTY", "LOT", "output.pdf")
```

## Performance

| Task | Time |
|------|------|
| Single label PDF | 200-500ms |
| Single label PNG | 300-600ms |
| Batch (4 labels) | ~1.5 sec |
| Print submission | ~100ms |

## Quality Levels

### Standard (300 DPI)
- Good for most applications
- Barcode easily scannable
- Default setting

### High Quality (600 DPI)
```python
gen = PDFLabelGenerator(dpi=600)
```
- Premium color reproduction
- Extra-high barcode precision

## Common Issues & Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| Barcode too small | Old config | Update to v2.0+ |
| Text cut off | >25 chars | Values auto-truncate |
| PDF won't print | Printer config | Check CUPS settings |
| Module not found | Missing venv | Run `source venv/bin/activate` |
| No barcodes | Generation error | Falls back to text |

## Environment Variables (Optional)

```bash
# Set default printer
export CUPS_DEFAULT_PRINTER="your_printer"

# Set temporary directory
export TMPDIR="/tmp/labels"
```

## Support Resources

1. **Error Messages** - Check console output
2. **GUI Issues** - Verify Kivy installation
3. **Print Issues** - Check CUPS configuration
4. **Barcode Issues** - Test with standard scanner

## System Requirements

- **Python:** 3.10+
- **OS:** Linux (CUPS required)
- **Printer:** Any CUPS-compatible printer
- **Display:** For GUI (optional, can run headless)

## Version Info

- **System Version:** 2.0 (PDF-based)
- **Release Date:** February 5, 2026
- **Status:** ✓ Production Ready

---

**Quick Notes:**
- Always activate venv before running
- Label size is 11.5cm × 8cm (fixed)
- Barcode height 18mm (fixed)
- Max 25 characters per field (auto-truncates)
- PDF format for best quality
- Use CUPS for printing
