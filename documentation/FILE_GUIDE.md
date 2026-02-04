# 📋 File Reference Guide

## Project Files Overview

All files in `/srv/Label-design/` are listed below with their purposes:

---

## 🆕 NEW FILES (Created for GUI Application)

### Core Application
| File | Size | Purpose |
|------|------|---------|
| [label_printer_gui.py](label_printer_gui.py) | ~400 lines | Main Kivy GUI application - Start here! |

### Setup & Launchers
| File | Purpose |
|------|---------|
| [setup_and_run.py](setup_and_run.py) | Python setup script (recommended way to start) |
| [start_gui.sh](start_gui.sh) | Bash launcher script (alternative method) |

### Dependencies
| File | Purpose |
|------|---------|
| [requirements_gui.txt](requirements_gui.txt) | Python packages needed for GUI (kivy, etc) |

### Documentation
| File | Best For |
|------|----------|
| [GETTING_STARTED.md](GETTING_STARTED.md) | 👈 **START HERE** - Quick start (15 min read) |
| [README_GUI.md](README_GUI.md) | Complete feature documentation (30 min read) |
| [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md) | Architecture, customization, development (1 hour read) |
| [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) | What was built and how to use it |

---

## 📦 ORIGINAL FILES (Preserved)

### Core Printing Engine
| File | Size | Purpose |
|------|------|---------|
| [print_label.py](print_label.py) | ~270 lines | Core label printing functions |

### Original Documentation
| File | Purpose |
|------|---------|
| [how_to.txt](how_to.txt) | Original usage instructions |
| [requirements.txt](requirements.txt) | Original dependencies (barcode, pillow, pycups) |

---

## 🎯 How to Start

### ✅ Recommended: Automatic Setup
```bash
cd /srv/Label-design
python3 setup_and_run.py
```

This will:
1. Check Python version
2. Verify CUPS printer service
3. Install dependencies
4. Launch the GUI

### 📖 Alternative: Manual Start

**Step 1:** Install dependencies
```bash
pip install -r requirements_gui.txt
```

**Step 2:** Run the application
```bash
python3 label_printer_gui.py
```

### 🐚 Alternative: Bash Script
```bash
chmod +x start_gui.sh
./start_gui.sh
```

---

## 📚 Documentation Reading Order

### For Users:
1. **[GETTING_STARTED.md](GETTING_STARTED.md)** ← Read this first! (15 min)
2. **[README_GUI.md](README_GUI.md)** ← For detailed features (30 min)
3. **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** ← Overview of what was built (15 min)

### For Developers:
1. **[TECHNICAL_DOCS.md](TECHNICAL_DOCS.md)** ← Architecture and implementation details
2. **[label_printer_gui.py](label_printer_gui.py)** ← Read the code with comments
3. **[print_label.py](print_label.py)** ← Understand printing engine

---

## 🗂️ File Relationships

```
Your Application Structure:

Entry Points:
├── setup_and_run.py ──────────► Checks env & starts GUI
├── start_gui.sh ───────────────► Bash alternative
└── label_printer_gui.py ──────► Main GUI (runs here)

GUI Application:
└── label_printer_gui.py
    ├── imports → print_label.py (printing functions)
    ├── imports → Kivy (UI framework)
    ├── LabelPreviewWidget class (preview display)
    └── LabelPrinterApp class (main app logic)

Printing Engine (unchanged):
└── print_label.py
    ├── create_label_image(text) → PIL Image
    └── print_label_standalone(value, printer, preview) → prints

Documentation:
├── GETTING_STARTED.md (quick start)
├── README_GUI.md (features)
├── TECHNICAL_DOCS.md (development)
└── IMPLEMENTATION_SUMMARY.md (overview)

Dependencies:
├── requirements_gui.txt (new - Kivy stack)
└── requirements.txt (original - printing)
```

---

## 🔍 Finding Things

### "How do I...?"

| Question | See File |
|----------|----------|
| ...get started quickly? | [GETTING_STARTED.md](GETTING_STARTED.md) |
| ...understand all features? | [README_GUI.md](README_GUI.md) |
| ...modify the GUI? | [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md) |
| ...understand the code? | [label_printer_gui.py](label_printer_gui.py) (with comments) |
| ...see what was implemented? | [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) |
| ...fix a problem? | [GETTING_STARTED.md](GETTING_STARTED.md#troubleshooting) |
| ...change label size? | [TECHNICAL_DOCS.md](TECHNICAL_DOCS.md#customization-guide) |
| ...use just the printing functions? | [print_label.py](print_label.py) |

---

## 💾 File Details

### label_printer_gui.py
```python
# Main GUI application
# ~400 lines
# Classes: LabelPreviewWidget, LabelPrinterApp
# Features: Data entry, live preview, printing, notifications
```

### setup_and_run.py
```python
# Automatic environment setup
# ~100 lines
# Checks: Python, CUPS, dependencies
# Action: Installs packages and launches GUI
```

### start_gui.sh
```bash
# Bash launcher
# ~40 lines
# Portable way to start GUI on Linux/Unix
# Handles: Path issues, package installation
```

### requirements_gui.txt
```
kivy
python-barcode
pillow
pycups
```

---

## 🚀 Quick Reference

| To Do This | Use This File | Command |
|-----------|--------------|---------|
| Start GUI | setup_and_run.py | `python3 setup_and_run.py` |
| Quick help | GETTING_STARTED.md | Read in editor |
| Learn features | README_GUI.md | Read in editor |
| Debug issues | TECHNICAL_DOCS.md | Read in editor |
| View code | label_printer_gui.py | Open in editor |
| Use printing API | print_label.py | Import functions |

---

## 📊 Statistics

```
Total Project Files: 11
├── Code: 3 (gui + 2 setup scripts)
├── Configuration: 2 (requirements files)
├── Documentation: 4 (guides + summary)
└── Original: 2 (preserved from original project)

Total Lines of Code: ~600
├── GUI Application: ~400 lines
├── Setup Scripts: ~140 lines
└── Launcher: ~40 lines

Total Documentation: ~5000 lines
├── Getting Started: ~400 lines
├── README GUI: ~600 lines
├── Technical Docs: ~2500 lines
├── Summary: ~1500 lines
└── This File: ~200 lines
```

---

## 🎯 Recommended Reading Path

```
Day 1:
└─ Setup and Run
   ├─ Read: GETTING_STARTED.md (15 min)
   ├─ Run: python3 setup_and_run.py (5 min)
   └─ Use: Print your first label! (5 min)

Day 2:
└─ Understand Features
   ├─ Read: README_GUI.md (30 min)
   └─ Use: Try all features in GUI (20 min)

Day 3:
└─ Customize
   ├─ Read: TECHNICAL_DOCS.md (1 hour)
   ├─ Edit: Modify label_printer_gui.py
   └─ Test: Try your modifications (30 min)
```

---

## ✅ Verification Checklist

To verify everything is set up:

```bash
# 1. Check files exist
ls -la /srv/Label-design/

# 2. Check Python installed
python3 --version

# 3. Check Git (optional)
git log --oneline -5

# 4. Install dependencies
python3 setup_and_run.py  # This installs for you

# 5. Run application
python3 label_printer_gui.py
```

---

## 💡 Tips

- **First time?** Start with `python3 setup_and_run.py`
- **Lost?** Check `GETTING_STARTED.md`
- **Questions?** Look in `README_GUI.md`
- **Customize?** Read `TECHNICAL_DOCS.md`
- **Code examples?** Check function comments in `label_printer_gui.py`

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Can't start GUI | Run: `python3 setup_and_run.py` (installs deps) |
| Want quick start | Read: `GETTING_STARTED.md` |
| Need all features | Read: `README_GUI.md` |
| Want to customize | Read: `TECHNICAL_DOCS.md` |
| Printer not found | Check: `GETTING_STARTED.md#Printer-Setup` |

---

**Last Updated:** February 4, 2026  
**Project Status:** ✅ Complete and Ready to Use

**👉 Next Step:** Run `python3 setup_and_run.py` to get started!
