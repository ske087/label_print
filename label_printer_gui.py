"""
Label Printer GUI Application using Kivy
Simplified mobile-friendly interface for printing labels.
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
from kivy.graphics import Color, Rectangle

import os
import threading
import platform
from print_label import print_label_standalone, get_available_printers
from kivy.clock import Clock

# Set window size - portrait/phone dimensions (375x667 like iPhone)
# Adjusted to be slightly wider for touch-friendly UI
Window.size = (420, 700)





class LabelPrinterApp(App):
    """Simplified Kivy application for label printing"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.available_printers = self.get_available_printers()
    
    def get_available_printers(self):
        """Get list of available printers (cross-platform)"""
        return get_available_printers()
    
    def build(self):
        """Build the simplified single-column UI"""
        self.title = "Label Printing"
        
        # Main container - single column layout
        main_layout = BoxLayout(orientation='vertical', spacing=8, padding=12)
        
        # Title
        title = Label(
            text='[b]Label Printing[/b]',
            markup=True,
            size_hint_y=0.08,
            font_size='18sp',
            color=(1, 1, 1, 1)
        )
        main_layout.add_widget(title)
        
        # Scroll view for form fields
        scroll = ScrollView(size_hint_y=0.75)
        form_layout = GridLayout(cols=1, spacing=8, size_hint_y=None, padding=8)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # SAP-Nr. Articol
        sap_label = Label(
            text='SAP-Nr. Articol:',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        form_layout.add_widget(sap_label)
        
        self.sap_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='14sp',
            background_color=(0.95, 0.95, 0.95, 1),
            padding=(10, 10)
        )
        self.sap_input.bind(text=self.on_sap_text_change)
        form_layout.add_widget(self.sap_input)
        
        # Cantitate
        qty_label = Label(
            text='Cantitate:',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        form_layout.add_widget(qty_label)
        
        self.qty_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='14sp',
            background_color=(0.95, 0.95, 0.95, 1),
            padding=(10, 10),
            input_filter='int'  # Only allow numbers
        )
        self.qty_input.bind(text=self.on_qty_text_change)
        form_layout.add_widget(self.qty_input)
        
        # ID rola cablu
        cable_id_label = Label(
            text='ID rola cablu:',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        form_layout.add_widget(cable_id_label)
        
        self.cable_id_input = TextInput(
            multiline=False,
            size_hint_y=None,
            height=45,
            font_size='14sp',
            background_color=(0.95, 0.95, 0.95, 1),
            padding=(10, 10)
        )
        self.cable_id_input.bind(text=self.on_cable_id_text_change)
        form_layout.add_widget(self.cable_id_input)
        
        # Printer selection
        printer_label = Label(
            text='Select Printer:',
            size_hint_y=None,
            height=30,
            font_size='12sp'
        )
        form_layout.add_widget(printer_label)
        
        printer_spinner = Spinner(
            text=self.available_printers[0] if self.available_printers else "No Printers",
            values=self.available_printers,
            size_hint_y=None,
            height=45,
            font_size='12sp'
        )
        self.printer_spinner = printer_spinner
        form_layout.add_widget(printer_spinner)
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        # Print button
        print_button = Button(
            text='PRINT LABEL',
            size_hint_y=0.15,
            font_size='14sp',
            background_color=(0.2, 0.6, 0.2, 1),
            background_normal='',
            bold=True
        )
        print_button.bind(on_press=self.print_label)
        main_layout.add_widget(print_button)
        
        return main_layout
    
    def on_sap_text_change(self, instance, value):
        """Limit SAP input to 25 characters"""
        if len(value) > 25:
            self.sap_input.text = value[:25]
    
    def on_qty_text_change(self, instance, value):
        """Limit Quantity input to 25 characters"""
        if len(value) > 25:
            self.qty_input.text = value[:25]
    
    def on_cable_id_text_change(self, instance, value):
        """Limit Cable ID input to 25 characters"""
        if len(value) > 25:
            self.cable_id_input.text = value[:25]
    
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
            size_hint=(0.8, 0.3)
        )
        
        popup.content.add_widget(Label(text='Processing label...\nPlease wait'))
        popup.open()
        
        # Print in background thread (using PDF by default)
        def print_thread():
            try:
                success = print_label_standalone(label_text, printer, preview=0, use_pdf=True)
                if success:
                    # Use Clock.schedule_once to update UI from main thread
                    Clock.schedule_once(lambda dt: popup.dismiss(), 0)
                    Clock.schedule_once(lambda dt: self.show_popup("Success", "Label printed successfully!"), 0.1)
                    # Clear inputs after successful print
                    Clock.schedule_once(lambda dt: self.clear_inputs(), 0.2)
                else:
                    Clock.schedule_once(lambda dt: popup.dismiss(), 0)
                    Clock.schedule_once(lambda dt: self.show_popup("Error", "Failed to print label"), 0.1)
            except Exception as e:
                Clock.schedule_once(lambda dt: popup.dismiss(), 0)
                Clock.schedule_once(lambda dt: self.show_popup("Error", f"Print error: {str(e)}"), 0.1)
        
        thread = threading.Thread(target=print_thread)
        thread.daemon = True
        thread.start()
    
    def clear_inputs(self):
        """Clear all input fields"""
        self.sap_input.text = ''
        self.qty_input.text = ''
        self.cable_id_input.text = ''
    
    def show_popup(self, title, message):
        """Show a popup message"""
        popup = Popup(
            title=title,
            content=BoxLayout(
                orientation='vertical',
                padding=10,
                spacing=10
            ),
            size_hint=(0.8, 0.4)
        )
        
        popup.content.add_widget(Label(text=message))
        
        close_button = Button(text='OK', size_hint_y=0.3)
        close_button.bind(on_press=popup.dismiss)
        popup.content.add_widget(close_button)
        
        popup.open()


if __name__ == '__main__':
    app = LabelPrinterApp()
    app.run()
