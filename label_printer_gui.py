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
from print_label import create_label_image, print_label_standalone

# Set window size
Window.size = (1600, 900)


class LabelPreviewWidget(ScatterLayout):
    """Widget for displaying the label preview"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label_image = None
        self.temp_preview_path = None
    
    def update_preview(self, text):
        """Update the preview with new label image"""
        if text:
            try:
                self.label_image = create_label_image(text)
                self.display_preview()
            except Exception as e:
                print(f"Error creating preview: {e}")
    
    def display_preview(self):
        """Display the preview image"""
        if self.label_image:
            # Save to temporary file
            import tempfile
            if self.temp_preview_path and os.path.exists(self.temp_preview_path):
                try:
                    os.remove(self.temp_preview_path)
                except:
                    pass
            
            with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                self.label_image.save(tmp.name)
                self.temp_preview_path = tmp.name
            
            # Clear and recreate children
            self.clear_widgets()
            
            # Add image
            img = KivyImage(source=self.temp_preview_path, size_hint=(1, 1))
            self.add_widget(img)


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
            input_filter='int',
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
        title = Label(text='[b]Label Preview (11.5cm x 8cm)[/b]', markup=True, 
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
        quantity = self.qty_input.text
        cable_id = self.cable_id_input.text
        
        # Create label text combining all fields
        if sap_nr or quantity or cable_id:
            label_text = f"{sap_nr}|{quantity}|{cable_id}"
            self.preview_widget.update_preview(label_text)
    
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
            input_filter='int',
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
        title = Label(text='[b]Label Preview (11.5cm x 8cm)[/b]', markup=True, 
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
        quantity = self.qty_input.text
        cable_id = self.cable_id_input.text
        
        # Create label text combining all fields
        if sap_nr or quantity or cable_id:
            label_text = f"{sap_nr}|{quantity}|{cable_id}"
            self.preview_widget.update_preview(label_text)
    
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
