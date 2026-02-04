"""
Label Printer GUI Application using Kivy
This application provides a user-friendly interface for printing labels with barcodes.
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.image import Image as KivyImage
from kivy.uix.widget import Widget
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.graphics import Color, Rectangle
from kivy.uix.scatterlayout import ScatterLayout

from PIL import Image as PILImage
import cups
import io
import os
import threading
import tempfile
import time
from print_label import create_label_image, print_label_standalone
from kivy.clock import Clock

# Set window size
Window.size = (1600, 900)


class LabelPreviewWidget(BoxLayout):
    """Widget for displaying the warehouse identification label preview"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.temp_file_path = None
    
    def update_preview(self, sap_nr, cantitate, lot_number):
        """Update preview with label and barcode information"""
        try:
            # Create label with article info
            label_text = f"{sap_nr}|{cantitate}|{lot_number}"
            self.generate_and_display_preview(sap_nr, cantitate, lot_number, label_text)
        except Exception as e:
            print(f"Error updating preview: {e}")
    
    def generate_and_display_preview(self, sap_nr, cantitate, lot_number, barcode_text):
        """Generate preview showing alternating text and barcode rows"""
        from PIL import Image, ImageDraw, ImageFont
        import barcode
        from barcode.writer import ImageWriter
        
        # Canvas dimensions (11.5cm x 8cm) * 1.5 = 17.25cm x 12cm
        # At 96 DPI: 11.5cm ≈ 435px, 8cm ≈ 303px
        # Increased by 50%: 652px x 454px
        canvas_width = 650
        canvas_height = 450
        
        # Left margin: 0.5cm ≈ 19px * 1.5 = 28px
        left_margin = 28
        usable_width = canvas_width - left_margin
        
        # Create canvas
        canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
        draw = ImageDraw.Draw(canvas)
        
        # 6 rows total
        row_height = canvas_height // 6
        
        # Font for text (larger for bigger canvas)
        try:
            label_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
            value_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            label_font = ImageFont.load_default()
            value_font = ImageFont.load_default()
        
        # Row definitions: (label_text, barcode_value, row_index)
        rows_data = [
            ("SAP-Nr. Article", sap_nr, 0),
            (None, sap_nr, 1),  # Barcode row
            ("Cantitate", cantitate, 2),
            (None, cantitate, 3),  # Barcode row
            ("ID rola cablu", lot_number, 4),
            (None, lot_number, 5),  # Barcode row
        ]
        
        for label_text, value, row_idx in rows_data:
            row_y = row_idx * row_height
            
            # Draw row border
            draw.rectangle(
                [(0, row_y), (canvas_width, row_y + row_height)],
                outline='black',
                width=1
            )
            
            if label_text:
                # Text row: show label and value
                draw.text(
                    (left_margin + 8, row_y + 8),
                    f"{label_text}: {value if value else '(empty)'}",
                    fill='black',
                    font=label_font
                )
            else:
                # Barcode row
                if value and value.strip():
                    try:
                        # Limit barcode text to 25 characters
                        barcode_value = str(value)[:25]
                        
                        CODE128 = barcode.get_barcode_class('code128')
                        writer_options = {
                            "write_text": False,
                            "module_width": 0.5,
                            "module_height": 12,  # Smaller height for better fit
                            "quiet_zone": 2,
                            "font_size": 0
                        }
                        code = CODE128(barcode_value, writer=ImageWriter())
                        filename = code.save('label_barcode_tmp', options=writer_options)
                        barcode_img = Image.open(filename)
                        
                        # Use standard barcode size, don't resize to fit width
                        canvas.paste(barcode_img, (left_margin + 4, row_y + 12))
                    except Exception as e:
                        print(f"Barcode error: {e}")
                        draw.text(
                            (left_margin + 8, row_y + row_height // 2 - 10),
                            "Barcode: " + str(value)[:25],
                            fill='black',
                            font=value_font
                        )
                else:
                    draw.text(
                        (left_margin + 8, row_y + row_height // 2 - 10),
                        "(no data)",
                        fill='gray',
                        font=value_font
                    )
        
        # Save and display
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            canvas.save(tmp.name)
            
            # Clean up old file
            if self.temp_file_path and os.path.exists(self.temp_file_path):
                try:
                    os.remove(self.temp_file_path)
                except:
                    pass
            
            self.temp_file_path = tmp.name
            
            # Update display
            self.clear_widgets()
            img_widget = KivyImage(source=tmp.name, size_hint=(1, 1))
            self.add_widget(img_widget)


class LabelPrinterApp(App):
    """Main Kivy application for label printing"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_printers = self.get_available_printers()
        self.preview_widget = None
    
    def get_available_printers(self):
        """Get list of available printers from CUPS"""
        try:
            conn = cups.Connection()
            printers = conn.getPrinters()
            return list(printers.keys()) if printers else ["PDF"]
        except Exception as e:
            print(f"Error getting printers: {e}")
            return ["PDF"]
    
    def build(self):
        """Build the main UI"""
        self.title = "Label Printer Interface"
        
        # Main layout - horizontal split between input and preview
        main_layout = BoxLayout(orientation='horizontal', spacing=10, padding=10)
        
        # Left column - Input form
        left_column = self.create_input_column()
        
        # Right column - Preview
        right_column = self.create_preview_column()
        
        main_layout.add_widget(left_column)
        main_layout.add_widget(right_column)
        
        return main_layout
    
    def create_input_column(self):
        """Create the left column with input fields"""
        container = BoxLayout(orientation='vertical', size_hint_x=0.4, spacing=10)
        
        # Title
        title = Label(text='[b]Label Information[/b]', markup=True, size_hint_y=0.08, 
                     font_size='18sp')
        container.add_widget(title)
        
        # Scroll view for form
        scroll = ScrollView(size_hint_y=0.85)
        form_layout = GridLayout(cols=1, spacing=10, size_hint_y=None, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # SAP-Nr. Articol
        sap_label = Label(text='SAP-Nr. Articol:', size_hint_y=None, height=40, 
                         font_size='14sp')
        form_layout.add_widget(sap_label)
        
        self.sap_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.sap_input.bind(text=self.on_input_change)
        form_layout.add_widget(self.sap_input)
        
        # Cantitate
        qty_label = Label(text='Cantitate:', size_hint_y=None, height=40, 
                         font_size='14sp')
        form_layout.add_widget(qty_label)
        
        self.qty_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.qty_input.bind(text=self.on_input_change)
        form_layout.add_widget(self.qty_input)
        
        # ID rola cablu
        cable_id_label = Label(text='ID rola cablu:', size_hint_y=None, height=40, 
                              font_size='14sp')
        form_layout.add_widget(cable_id_label)
        
        self.cable_id_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=50,
            font_size='16sp',
            background_color=(0.95, 0.95, 0.95, 1)
        )
        self.cable_id_input.bind(text=self.on_input_change)
        form_layout.add_widget(self.cable_id_input)
        
        # Printer selection
        printer_label = Label(text='Select Printer:', size_hint_y=None, height=40, 
                             font_size='14sp')
        form_layout.add_widget(printer_label)
        
        printer_spinner = Spinner(
            text=self.available_printers[0] if self.available_printers else "No Printers",
            values=self.available_printers,
            size_hint_y=None,
            height=50,
            font_size='14sp'
        )
        self.printer_spinner = printer_spinner
        form_layout.add_widget(printer_spinner)
        
        scroll.add_widget(form_layout)
        container.add_widget(scroll)
        
        # Print button
        print_button = Button(
            text='PRINT LABEL',
            size_hint_y=0.15,
            font_size='16sp',
            background_color=(0.2, 0.6, 0.2, 1),
            background_normal='',
            bold=True
        )
        print_button.bind(on_press=self.print_label)
        container.add_widget(print_button)
        
        return container
    
    def create_preview_column(self):
        """Create the right column with preview"""
        container = BoxLayout(orientation='vertical', size_hint_x=0.6, spacing=10)
        
        # Title
        title = Label(text='[b]Label Preview[/b]', markup=True, 
                     size_hint_y=0.08, font_size='18sp')
        container.add_widget(title)
        
        # Preview canvas
        self.preview_widget = LabelPreviewWidget(size_hint_y=0.92)
        container.add_widget(self.preview_widget)
        
        return container
    
    def on_input_change(self, instance, value):
        """Update preview when input changes"""
        # Get all input values
        sap_nr = self.sap_input.text
        cantitate = self.qty_input.text  # This is actually the barcode/cantitate field
        cable_id = self.cable_id_input.text
        
        # Update preview
        self.preview_widget.update_preview(sap_nr, cantitate, cable_id)
    
    def print_label(self, instance):
        """Handle print button press"""
        sap_nr = self.sap_input.text.strip()
        quantity = self.qty_input.text.strip()
        cable_id = self.cable_id_input.text.strip()
        printer = self.printer_spinner.text
        
        # Validate input
        if not sap_nr and not quantity and not cable_id:
            self.show_popup("Error", "Please enter at least one field")
            return
        
        # Create combined label text
        label_text = f"{sap_nr}|{quantity}|{cable_id}"
        
        # Show loading popup
        popup = Popup(
            title='Printing',
            content=BoxLayout(
                orientation='vertical',
                padding=10,
                spacing=10
            ),
            size_hint=(0.6, 0.3)
        )
        
        popup.content.add_widget(Label(text='Printing label...\nPlease wait'))
        popup.open()
        
        # Print in background thread
        def print_thread():
            try:
                success = print_label_standalone(label_text, printer, preview=0)
                if success:
                    popup.dismiss()
                    self.show_popup("Success", "Label printed successfully!")
                else:
                    popup.dismiss()
                    self.show_popup("Error", "Failed to print label")
            except Exception as e:
                popup.dismiss()
                self.show_popup("Error", f"Print error: {str(e)}")
        
        thread = threading.Thread(target=print_thread)
        thread.daemon = True
        thread.start()
    
    def show_popup(self, title, message):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=BoxLayout(
                orientation='vertical',
                padding=10,
                spacing=10
            ),
            size_hint=(0.6, 0.3)
        )
        
        popup.content.add_widget(Label(text=message))
        
        close_button = Button(text='OK', size_hint_y=0.3)
        close_button.bind(on_press=popup.dismiss)
        popup.content.add_widget(close_button)
        
        popup.open()


if __name__ == '__main__':
    app = LabelPrinterApp()
    app.run()
