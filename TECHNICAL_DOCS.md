# Technical Documentation - Label Printer GUI

## Architecture Overview

### Component Structure

```
label_printer_gui.py
├── LabelPreviewWidget (ScatterLayout)
│   ├── update_preview(text)
│   ├── display_preview()
│   └── Displays PIL image as Kivy widget
│
└── LabelPrinterApp (App)
    ├── build() → Main UI layout
    ├── create_input_column() → Left side form
    ├── create_preview_column() → Right side preview
    ├── get_available_printers() → CUPS integration
    ├── on_input_change() → Live preview update
    ├── print_label() → Print workflow
    └── show_popup() → User notifications
```

### Data Flow

```
User Input (TextInput)
    ↓
on_input_change() event
    ↓
Combine fields: f"{sap}|{qty}|{cable_id}"
    ↓
create_label_image() from print_label.py
    ↓
LabelPreviewWidget.update_preview()
    ↓
Display in right column
```

## Class Details

### LabelPreviewWidget

**Purpose:** Display real-time label preview

**Methods:**
- `update_preview(text)` - Create new label image from text
- `display_preview()` - Render image in Kivy widget

**Attributes:**
- `label_image` - Current PIL Image object
- `temp_preview_path` - Temporary PNG file path

**Key Features:**
- Uses PIL to generate labels at 300 DPI
- Displays in KivyImage widget
- Maintains aspect ratio (11.5cm × 8cm)
- Auto-updates on input change

### LabelPrinterApp

**Purpose:** Main application orchestrator

**Methods:**

| Method | Purpose |
|--------|---------|
| `build()` | Construct main UI layout |
| `create_input_column()` | Build left form panel |
| `create_preview_column()` | Build right preview panel |
| `get_available_printers()` | Fetch CUPS printer list |
| `on_input_change()` | Handle input updates |
| `print_label()` | Execute print workflow |
| `show_popup()` | Display notifications |

**Event Flow:**

1. **Initialization:**
   ```
   __init__() → get_available_printers()
                → build()
                → create_input_column()
                → create_preview_column()
   ```

2. **User Interaction:**
   ```
   TextInput.on_text → on_input_change()
                    → preview_widget.update_preview()
   ```

3. **Printing:**
   ```
   Button.on_press → print_label()
                   → threading.Thread(print_thread)
                   → print_label_standalone()
                   → show_popup()
   ```

## Integration with print_label.py

### Functions Used

```python
from print_label import create_label_image, print_label_standalone
```

**create_label_image(text)**
- Input: Combined text (e.g., "SAP123|50|REEL001")
- Output: PIL Image (11.5cm × 8cm @ 300 DPI)
- Generates Code128 barcode
- Centers text below barcode

**print_label_standalone(value, printer, preview)**
- Input:
  - `value`: Text to encode in barcode
  - `printer`: CUPS printer name (e.g., "PDF")
  - `preview`: 0=no preview, 1-3=3s, >3=5s
- Output: Boolean (True=success)
- Handles CUPS printing
- Manages temporary files

## UI Layout Structure

### Main Layout
```
BoxLayout (horizontal)
├── Left Column (40%)
│   BoxLayout (vertical)
│   ├── Title Label
│   ├── ScrollView
│   │   └── GridLayout (1 col)
│   │       ├── Label: "SAP-Nr. Articol"
│   │       ├── TextInput (sap_input)
│   │       ├── Label: "Cantitate"
│   │       ├── TextInput (qty_input)
│   │       ├── Label: "ID rola cablu"
│   │       ├── TextInput (cable_id_input)
│   │       ├── Label: "Select Printer"
│   │       └── Spinner (printer_spinner)
│   └── Button: "PRINT LABEL"
│
└── Right Column (60%)
    BoxLayout (vertical)
    ├── Title Label
    └── LabelPreviewWidget
```

### Styling

**Colors:**
- Print Button: `(0.2, 0.6, 0.2, 1)` - Green
- Background: Default Kivy theme
- Text: Black on white/gray

**Fonts:**
- Title: 18sp, bold
- Labels: 14sp, regular
- Input: 16sp, regular

**Sizing:**
- Window: 1600×900 (adjustable)
- Left column: 40% of width
- Right column: 60% of width

## Threading Model

### Background Printing

```python
def print_label(self, instance):
    # ... validation ...
    
    popup = Popup(...)  # Show loading
    popup.open()
    
    def print_thread():
        try:
            success = print_label_standalone(...)
            # Update UI in main thread
            popup.dismiss()
            self.show_popup(...)
        except Exception as e:
            # Error handling
            self.show_popup("Error", str(e))
    
    thread = threading.Thread(target=print_thread)
    thread.daemon = True
    thread.start()
```

**Why threading?**
- Prevents UI freezing during print
- CUPS operations can be slow
- User can continue working while printing

## Error Handling

### Validation

1. **Input Validation:**
   ```python
   if not sap_nr and not quantity and not cable_id:
       show_popup("Error", "Please enter at least one field")
   ```

2. **Printer Validation:**
   - Fallback to "PDF" if none available
   - Checks printer existence before print

3. **Exception Handling:**
   - Try-except in preview generation
   - Try-except in print thread
   - User-friendly error messages

### Logging

- Console output for debugging
- Error messages in popups
- Exception info in thread callbacks

## Performance Considerations

### Preview Updates

- Only regenerates label when text changes
- Debouncing happens naturally via Kivy events
- PIL image operations are fast (~100ms)

### Memory Management

- Temporary files auto-deleted
- PIL images cached during preview
- Temp preview file cleaned when updated

### CUPS Operations

- Non-blocking via threading
- Timeout handling for printer ops
- Connection pooled by pycups

## Customization Guide

### Change Label Size

In `print_label.py`:
```python
# Modify label dimensions
label_width = 1063   # pixels for 9cm @ 300 DPI
label_height = 591   # pixels for 5cm @ 300 DPI
```

For 11.5cm × 8cm @ 300 DPI:
```python
label_width = 1378   # 11.5cm @ 300 DPI
label_height = 944   # 8cm @ 300 DPI
```

### Modify UI Colors

In `label_printer_gui.py`:
```python
# Change print button color
Button(
    ...
    background_color=(R, G, B, A),  # RGBA: 0.0-1.0
    ...
)
```

### Add New Input Fields

```python
# In create_input_column():
new_label = Label(text='New Field:', size_hint_y=None, height=40)
form_layout.add_widget(new_label)

self.new_input = TextInput(...)
self.new_input.bind(text=self.on_input_change)
form_layout.add_widget(self.new_input)

# In on_input_change():
new_field = self.new_input.text
```

## Dependencies Deep Dive

### Kivy
- **Version:** 2.0+
- **Role:** GUI framework
- **Key classes:** App, BoxLayout, TextInput, Button, Spinner

### python-barcode
- **Version:** Latest
- **Role:** Code128 barcode generation
- **Integration:** Used in print_label.py

### Pillow (PIL)
- **Version:** 8.0+
- **Role:** Image generation and processing
- **Features:** ImageDraw for text, Image for resizing

### pycups
- **Version:** Latest
- **Role:** CUPS printer interface
- **Functions:** getPrinters(), printFile()

## Testing

### Unit Test Example

```python
def test_label_preview_update():
    app = LabelPrinterApp()
    test_text = "TEST|123|REEL"
    app.preview_widget.update_preview(test_text)
    assert app.preview_widget.label_image is not None

def test_printer_list():
    app = LabelPrinterApp()
    printers = app.get_available_printers()
    assert isinstance(printers, list)
    assert len(printers) > 0
```

### Manual Testing

1. **Preview Update Test:**
   - Type in each field
   - Verify preview updates
   - Check barcode changes

2. **Printer Test:**
   - Select different printers
   - Verify dropdown updates

3. **Print Test:**
   - Use PDF printer for testing
   - Check output file generated

## Deployment Notes

### System Requirements
- Linux/Unix (CUPS-based)
- X11 or Wayland display
- ~50MB disk space
- 2GB RAM minimum

### Installation Steps
1. Clone/download repository
2. Install Python 3.7+
3. Run setup_and_run.py
4. Configure system printer

### Containerization

For Docker deployment:
```dockerfile
FROM python:3.9-slim
RUN apt-get update && apt-get install -y cups
COPY . /app
WORKDIR /app
RUN pip install -r requirements_gui.txt
CMD ["python3", "label_printer_gui.py"]
```

## Future Enhancements

1. **Database Integration**
   - Store label history
   - Batch printing from CSV

2. **Label Templates**
   - Multiple label formats
   - Custom field layouts

3. **Advanced Features**
   - QR code support
   - Image/logo inclusion
   - Multi-language support

4. **Mobile Integration**
   - REST API server
   - Web interface

---

**Last Updated:** February 4, 2026
**Version:** 1.0
**Status:** Production Ready
