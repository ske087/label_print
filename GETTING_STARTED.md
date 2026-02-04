# Getting Started with Label Printer GUI

## Overview

Your Label Printer application now has a modern Kivy-based GUI interface! This guide will help you get started.

## Quick Start (3 Steps)

### Option 1: Python Script (Recommended)
```bash
python3 setup_and_run.py
```
This handles everything - checks dependencies, installs packages, and starts the GUI.

### Option 2: Bash Script
```bash
chmod +x start_gui.sh
./start_gui.sh
```

### Option 3: Manual
```bash
pip install -r requirements_gui.txt
python3 label_printer_gui.py
```

## What You'll See

### Main Window Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Label Printer Interface                   │
├──────────────────┬──────────────────────────────────────────┤
│   Input Column   │      Preview Column                       │
│   (40%)          │      (60%)                                │
│                  │                                           │
│ ✓ SAP-Nr. Input │      ╔════════════════════╗               │
│   [________]    │      ║   Live Preview     ║               │
│                  │      ║   11.5cm x 8cm     ║               │
│ ✓ Quantity      │      ║                    ║               │
│   [________]    │      ║  [Barcode]         ║               │
│                  │      ║   SAP | QTY | ID   ║               │
│ ✓ Cable ID      │      ║                    ║               │
│   [________]    │      ╚════════════════════╝               │
│                  │                                           │
│ ✓ Printer ▼     │                                           │
│   [PDF    ▼]    │                                           │
│                  │                                           │
│ [PRINT LABEL]   │                                           │
│                  │                                           │
└──────────────────┴──────────────────────────────────────────┘
```

## Features Explained

### Left Column - Data Entry

1. **SAP-Nr. Articol**
   - Enter the SAP article number or identifier
   - Example: `A012345`
   - Updates preview automatically

2. **Cantitate (Quantity)**
   - Numbers only
   - Example: `100`
   - Numeric input only

3. **ID rola cablu (Cable Reel ID)**
   - Cable reel identifier
   - Example: `REEL-001`
   - Updates preview automatically

4. **Printer Selection**
   - Dropdown menu with available system printers
   - Shows all CUPS-configured printers
   - Default: PDF printer (if no others available)

5. **Print Label Button**
   - Green button at bottom
   - Triggers printing to selected printer
   - Shows status notifications

### Right Column - Live Preview

- Shows exactly what will print
- Updates in real-time as you type
- Label dimensions: 11.5 cm × 8 cm
- Displays:
  - Barcode (Code128 format)
  - SAP number, quantity, and cable ID combined
  - High quality 300 DPI rendering

## Workflow Example

1. **Start the application:**
   ```bash
   python3 setup_and_run.py
   ```

2. **Enter data:**
   - SAP-Nr: `A456789`
   - Cantitate: `50`
   - ID rola cablu: `REEL-042`

3. **Check preview** (automatically updates on right)

4. **Select printer** (use dropdown)

5. **Click PRINT LABEL** button

6. **Confirm** when notification appears

## Printer Setup

### Check Available Printers
```bash
lpstat -p -d
```

### Add a Printer (if needed)
```bash
# Use CUPS web interface
http://localhost:631
```

### Common Printer Names
- `PDF` - Virtual PDF printer (for testing)
- `Brother_HL_L2350DW` - Brother laser printer
- `Canon_PIXMA` - Canon printer
- Check your system for exact name

## Troubleshooting

### "No Printers Found"
```bash
# Start CUPS service
sudo systemctl start cups

# Check status
sudo systemctl status cups

# List printers
lpstat -p -d
```

### Preview Not Updating
- Check Python console for errors
- Verify all dependencies installed: `pip list | grep -E 'kivy|barcode|pillow'`
- Try restarting the application

### Print Fails
```bash
# Test print command manually
echo "test" | lp -d PDF

# Check printer status
lpstat -p -l
```

### Kivy Window Issues
- If window doesn't open, check X11 display:
  ```bash
  echo $DISPLAY
  ```
- Resize window manually if elements overlap

## File Guide

- **label_printer_gui.py** - Main GUI application
- **print_label.py** - Core printing functions
- **setup_and_run.py** - Automatic setup script
- **start_gui.sh** - Bash launcher script
- **requirements_gui.txt** - Python dependencies
- **README_GUI.md** - Complete documentation

## Tips & Tricks

1. **Fast Printing:**
   - Preset SAP number as most common value
   - Just change quantity/ID for each label

2. **Batch Printing:**
   - Print one label at a time
   - Small UI makes it quick

3. **Testing:**
   - Use "PDF" printer to save test labels
   - Check output files to verify format

4. **Keyboard:**
   - Tab between fields
   - Enter in printer dropdown to confirm selection
   - Alt+P might activate Print button (Kivy dependent)

## Next Steps

- **Learn More:** See [README_GUI.md](README_GUI.md)
- **Customize:** Modify `label_printer_gui.py` for your needs
- **Integrate:** Use functions in other Python applications
- **Support:** Check console output for detailed error messages

---

**Ready to print?** Start with: `python3 setup_and_run.py`

