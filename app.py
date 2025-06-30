import tkinter as tk
from tkinter import simpledialog, messagebox, ttk, font
from PIL import Image, ImageTk, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import cups
import os
import time

# Valid operator codes (in a real app, this would be in a database)
VALID_OPERATORS = {
    "OP001": "Operator 1",
    "OP002": "Operator 2",
    "OP003": "Operator 3",
    "123456": "Admin"  # Simple code for testing
}

class LabelApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Configure fullscreen toggling
        self.allow_fullscreen_toggle = True  # Variable to control ESC key behavior
        
        # Configure the main window
        self.title("Label Printing System")
        self.configure(bg="#f0f0f0")
        
        # Create a container for all frames
        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Current logged in operator
        self.current_operator = None
        
        # Initialize frames dictionary
        self.frames = {}
        
        # Create frames
        for F in (LoginFrame, DashboardFrame, SettingsFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure container grid
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Show login frame
        self.show_frame(LoginFrame)
        
        # Bind Escape key to toggle fullscreen, respecting the variable
        self.bind('<Escape>', self.handle_escape)
        
        # Use after() to ensure fullscreen works - solves issues on some systems
        self.attributes('-fullscreen', True)
        self.after(100, self.ensure_fullscreen)
        
    def show_frame(self, frame_class):
        """Bring the specified frame to the front"""
        frame = self.frames[frame_class]
        frame.tkraise()
    
    def login(self, operator_code):
        """Attempt to login with the provided operator code"""
        if operator_code in VALID_OPERATORS:
            self.current_operator = {
                "code": operator_code,
                "name": VALID_OPERATORS[operator_code],
                "login_time": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Disable fullscreen toggle for admin users
            if operator_code == "123456":  # Admin code
                self.set_fullscreen_toggle(False)
            else:
                self.set_fullscreen_toggle(True)
                
            self.show_frame(DashboardFrame)
            self.frames[DashboardFrame].update_operator_info()
            return True
        return False
    
    def logout(self):
        """Log out and return to login screen"""
        self.current_operator = None
        self.show_frame(LoginFrame)

    def handle_escape(self, event):
        """Handle ESC key press based on toggle variable"""
        if self.allow_fullscreen_toggle:
            self.toggle_fullscreen()
    
    def toggle_fullscreen(self):
        """Toggle fullscreen mode"""
        if self.attributes('-fullscreen'):
            self.attributes('-fullscreen', False)
        else:
            self.attributes('-fullscreen', True)

    def set_fullscreen_toggle(self, enabled):
        """Enable or disable the ESC key fullscreen toggle"""
        self.allow_fullscreen_toggle = enabled
    
    def ensure_fullscreen(self):
        """Make sure we're in fullscreen mode"""
        if not self.attributes('-fullscreen'):
            self.attributes('-fullscreen', True)
    
    def is_admin(self):
        """Check if the current user is an admin"""
        if self.current_operator and self.current_operator["code"] == "123456":
            return True
        return False


class LoginFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Create login form
        login_frame = tk.Frame(self, bg="#ffffff", padx=30, pady=30)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title_font = font.Font(family="Arial", size=24, weight="bold")
        tk.Label(login_frame, text="Label Printing System", font=title_font, bg="#ffffff").pack(pady=(0, 20))
        
        # Operator code entry
        tk.Label(login_frame, text="Scan Operator Code:", font=("Arial", 14), bg="#ffffff").pack(anchor="w", pady=(10, 5))
        self.code_var = tk.StringVar()
        code_entry = tk.Entry(login_frame, textvariable=self.code_var, font=("Arial", 16), width=20, show="*")
        code_entry.pack(pady=(0, 20), fill="x")
        code_entry.focus_set()
        
        # Login button
        login_btn = tk.Button(login_frame, text="Login", font=("Arial", 14), 
                             bg="#4CAF50", fg="white", padx=20, pady=5,
                             command=self.login)
        login_btn.pack(pady=(10, 5))
        
        # Exit button
        exit_btn = tk.Button(login_frame, text="Exit", font=("Arial", 14), 
                            bg="#f44336", fg="white", padx=20, pady=5,
                            command=self.controller.destroy)
        exit_btn.pack(pady=(5, 0))
        
        # Bind Enter key to login
        code_entry.bind("<Return>", lambda event: self.login())
    
    def login(self):
        operator_code = self.code_var.get()
        if not operator_code:
            messagebox.showerror("Error", "Please enter an operator code")
            return
        
        if self.controller.login(operator_code):
            self.code_var.set("")  # Clear the entry
        else:
            messagebox.showerror("Error", "Invalid operator code")
            self.code_var.set("")  # Clear the entry


class DashboardFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Create header frame
        header_frame = tk.Frame(self, bg="#333333", height=60)
        header_frame.pack(fill="x")
        
        # App title
        tk.Label(header_frame, text="Label Printing Dashboard", font=("Arial", 16, "bold"), 
                fg="white", bg="#333333").pack(side="left", padx=20, pady=10)
        
        # Operator info
        self.operator_label = tk.Label(header_frame, text="", font=("Arial", 12), 
                                     fg="white", bg="#333333")
        self.operator_label.pack(side="right", padx=20, pady=10)
        
        # Settings button (only visible to admin)
        self.settings_btn = tk.Button(header_frame, text="Settings", font=("Arial", 12), 
                                    bg="#2196F3", fg="white", padx=10, pady=2,
                                    command=lambda: controller.show_frame(SettingsFrame))
        self.settings_btn.pack(side="right", padx=10, pady=10)
        self.settings_btn.pack_forget()  # Hide initially
        
        # Logout button
        logout_btn = tk.Button(header_frame, text="Logout", font=("Arial", 12), 
                              bg="#f44336", fg="white", padx=10, pady=2,
                              command=self.controller.logout)
        logout_btn.pack(side="right", padx=10, pady=10)
        
        # Create main container to hold all three frames
        main_container = tk.Frame(self, bg="#f0f0f0", padx=10, pady=10)
        main_container.pack(fill="both", expand=True)
        
        # Configure grid for the main container (2 rows, 2 columns)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(0, weight=2)  # Top row larger
        main_container.rowconfigure(1, weight=1)  # Bottom row smaller
        
        # 1. Create Label frame (top left)
        label_frame = tk.LabelFrame(main_container, text="Create Label", font=("Arial", 14), 
                                   bg="#f0f0f0", padx=20, pady=20)
        label_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        
        # 2. Available Articles frame (top right)
        articles_frame = tk.LabelFrame(main_container, text="Articole disponibile in viitor", 
                                     font=("Arial", 14), bg="#f0f0f0", padx=20, pady=20)
        articles_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        
        # 3. Last 6 Labels frame (bottom, spans two columns)
        history_frame = tk.LabelFrame(main_container, text="Ultimele 6 etichete printate", 
                                    font=("Arial", 14), bg="#f0f0f0", padx=20, pady=20)
        history_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        
        # Fill the Create Label frame with existing content
        # Text input
        tk.Label(label_frame, text="Enter text for label:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        self.text_var = tk.StringVar()
        text_entry = tk.Entry(label_frame, textvariable=self.text_var, font=("Arial", 14), width=40)
        text_entry.pack(fill="x", pady=(0, 20))
        text_entry.focus_set()
        
        # Preview checkbox
        self.preview_var = tk.BooleanVar(value=True)
        preview_chk = tk.Checkbutton(label_frame, text="Show print preview", variable=self.preview_var, 
                                    font=("Arial", 12), bg="#f0f0f0")
        preview_chk.pack(anchor="w", pady=(0, 20))
        
        # Buttons frame
        buttons_frame = tk.Frame(label_frame, bg="#f0f0f0")
        buttons_frame.pack(fill="x", pady=10)
        
        # Print button
        print_btn = tk.Button(buttons_frame, text="Print Label", font=("Arial", 14), 
                             bg="#4CAF50", fg="white", padx=20, pady=10,
                             command=self.print_label)
        print_btn.pack(side="left", padx=(0, 10))
        
        # Clear button
        clear_btn = tk.Button(buttons_frame, text="Clear", font=("Arial", 14), 
                             bg="#ff9800", fg="white", padx=20, pady=10,
                             command=lambda: self.text_var.set(""))
        clear_btn.pack(side="left")
        
        # Placeholder message for the other frames (to be filled later)
        tk.Label(articles_frame, text="Future articles will be displayed here", 
                font=("Arial", 12), bg="#f0f0f0").pack(expand=True)
        
        tk.Label(history_frame, text="Last 6 printed labels will be displayed here", 
                font=("Arial", 12), bg="#f0f0f0").pack(expand=True)
        
        # Status frame at the bottom
        status_frame = tk.Frame(self, bg="#e0e0e0", height=30)
        status_frame.pack(fill="x", side="bottom")
        
        self.status_label = tk.Label(status_frame, text="Ready", font=("Arial", 10), bg="#e0e0e0")
        self.status_label.pack(side="left", padx=10, pady=5)
    
    def update_operator_info(self):
        """Update the operator information displayed in the header"""
        if self.controller.current_operator:
            operator = self.controller.current_operator
            self.operator_label.config(text=f"Operator: {operator['name']} ({operator['code']})")
            
            # Show settings button only for admin
            if self.controller.is_admin():
                self.settings_btn.pack(side="right", padx=10, pady=10)
            else:
                self.settings_btn.pack_forget()
    
    def print_label(self):
        """Print a label with the entered text"""
        text = self.text_var.get().strip()
        if not text:
            messagebox.showerror("Error", "Please enter text for the label")
            return
        
        # Get saved printer or available printers
        saved_printer = get_saved_printer()
        
        if saved_printer:
            printer = saved_printer
        else:
            # Get available printers
            try:
                printers = get_printers()
                if not printers:
                    messagebox.showerror("Error", "No printers found")
                    return
            except Exception as e:
                messagebox.showerror("Error", f"Could not get printers: {str(e)}")
                return
            
            # Select printer
            printer = select_printer(printers)
            if not printer:
                return  # User cancelled
        
        # Create and print label
        try:
            self.status_label.config(text="Creating label...")
            self.update_idletasks()
            
            label_img = create_label_image(text)
            label_img.save('final_label.png')
            
            if self.preview_var.get():
                self.status_label.config(text="Showing preview...")
                self.update_idletasks()
                show_preview('final_label.png', lambda: self.complete_print(printer, text))
            else:
                self.complete_print(printer, text)
                
        except Exception as e:
            messagebox.showerror("Error", f"Error creating label: {str(e)}")
            self.status_label.config(text="Ready")
    
    def complete_print(self, printer, text):
        """Complete the print job after preview (if shown)"""
        try:
            self.status_label.config(text="Printing...")
            self.update_idletasks()
            
            print_label(printer, text)
            
            self.status_label.config(text="Label printed successfully")
            show_auto_close_info("Success", "Label sent to printer", timeout=2000)
            
            # Clear text field after successful print
            self.text_var.set("")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error printing label: {str(e)}")
        finally:
            self.status_label.config(text="Ready")


class SettingsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#f0f0f0")
        self.controller = controller
        
        # Create header frame
        header_frame = tk.Frame(self, bg="#333333", height=60)
        header_frame.pack(fill="x")
        
        # App title
        tk.Label(header_frame, text="Settings", font=("Arial", 16, "bold"), 
                fg="white", bg="#333333").pack(side="left", padx=20, pady=10)
        
        # Back button
        back_btn = tk.Button(header_frame, text="Back to Dashboard", font=("Arial", 12), 
                            bg="#4CAF50", fg="white", padx=10, pady=2,
                            command=lambda: controller.show_frame(DashboardFrame))
        back_btn.pack(side="right", padx=10, pady=10)
        
        # Create main content frame
        content_frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        content_frame.pack(fill="both", expand=True)
        
        # Printer settings section
        printer_frame = tk.LabelFrame(content_frame, text="Printer Settings", font=("Arial", 14), bg="#f0f0f0", padx=20, pady=20)
        printer_frame.pack(fill="x", expand=False, padx=20, pady=20)
        
        # Printer selection
        tk.Label(printer_frame, text="Select Default Printer:", font=("Arial", 12), bg="#f0f0f0").pack(anchor="w", pady=(0, 5))
        
        # Get available printers
        try:
            self.printers = get_printers()
            self.printer_var = tk.StringVar()
            
            # Load saved printer if available
            saved_printer = load_printer_config()
            if saved_printer and saved_printer in self.printers:
                self.printer_var.set(saved_printer)
            elif self.printers:
                self.printer_var.set(self.printers[0])
                
            combo = ttk.Combobox(printer_frame, textvariable=self.printer_var, values=self.printers, 
                                state="readonly", font=("Arial", 12), width=40)
            combo.pack(pady=(0, 20), fill="x")
            
            # Save button
            save_btn = tk.Button(printer_frame, text="Save Printer Setting", font=("Arial", 12), 
                                bg="#4CAF50", fg="white", padx=10, pady=5,
                                command=self.save_printer_config)
            save_btn.pack(pady=10)
            
        except Exception as e:
            tk.Label(printer_frame, text=f"Error loading printers: {str(e)}", font=("Arial", 12), 
                    fg="red", bg="#f0f0f0").pack(pady=10)
    
    def save_printer_config(self):
        """Save the selected printer to a configuration file"""
        selected_printer = self.printer_var.get()
        if selected_printer:
            try:
                with open('printer_config.txt', 'w') as f:
                    f.write(selected_printer)
                messagebox.showinfo("Success", "Printer setting saved successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Could not save printer setting: {str(e)}")


# Your existing functions remain largely the same
def get_printers():
    conn = cups.Connection()
    return list(conn.getPrinters().keys())

def create_label_image(text):
    # Your existing create_label_image function (unchanged)
    # Label dimensions for 9x5 cm at 300 DPI
    label_width = 1063   # 9 cm
    label_height = 591   # 5 cm

    # Outer frame (95% of label, centered)
    outer_frame_width = int(label_width * 0.95)
    outer_frame_height = int(label_height * 0.95)
    outer_frame_x = (label_width - outer_frame_width) // 2
    outer_frame_y = (label_height - outer_frame_height) // 2

    # Barcode frame (top, inside outer frame)
    barcode_frame_width = int(outer_frame_width * 0.90)
    barcode_frame_height = int(outer_frame_height * 0.60)
    barcode_frame_x = outer_frame_x + (outer_frame_width - barcode_frame_width) // 2
    barcode_frame_y = outer_frame_y

    # Text frame (immediately below barcode frame)
    text_frame_width = int(outer_frame_width * 0.90)
    text_frame_height = int(outer_frame_height * 0.35)
    text_frame_x = outer_frame_x + (outer_frame_width - text_frame_width) // 2
    gap_between_frames = 5  # or 0 for no gap
    text_frame_y = barcode_frame_y + barcode_frame_height + gap_between_frames

    # Generate barcode image (no text), at higher resolution
    CODE128 = barcode.get_barcode_class('code128')
    writer_options = {
        "write_text": False,
        "module_width": 0.5,  # default is 0.2, increase for higher res
        "module_height": barcode_frame_height,  # match frame height
        "quiet_zone": 3.5,    # default, can adjust if needed
        "font_size": 0        # no text
    }
    code = CODE128(text, writer=ImageWriter())
    filename = code.save('label_barcode', options=writer_options)
    barcode_img = Image.open(filename)

    # Now resize barcode to exactly fit barcode frame (stretch, do not keep aspect ratio)
    barcode_resized = barcode_img.resize((barcode_frame_width, barcode_frame_height), Image.LANCZOS)

    # Create label image
    label_img = Image.new('RGB', (label_width, label_height), 'white')

    # Paste barcode centered in barcode frame
    label_img.paste(barcode_resized, (barcode_frame_x, barcode_frame_y))

    # Draw text in text frame, maximize font size to fit frame (keep sharpness)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    max_font_size = text_frame_height
    min_font_size = 10
    best_font_size = min_font_size
    for font_size in range(min_font_size, max_font_size + 1):
        try:
            font = ImageFont.truetype(font_path, font_size)
        except IOError:
            font = ImageFont.load_default()
            break
        dummy_img = Image.new('RGB', (1, 1))
        dummy_draw = ImageDraw.Draw(dummy_img)
        text_bbox = dummy_draw.textbbox((0, 0), text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        if text_width > text_frame_width or text_height > text_frame_height:
            break
        best_font_size = font_size

    # Use the best font size found
    try:
        font = ImageFont.truetype(font_path, best_font_size)
    except IOError:
        font = ImageFont.load_default()
    draw = ImageDraw.Draw(label_img)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = text_frame_x + (text_frame_width - text_width) // 2
    text_y = text_frame_y + (text_frame_height - text_height) // 2
    draw.text((text_x, text_y), text, font=font, fill='black')

    os.remove(filename)
    return label_img

def print_label(printer_name, text):
    label_img = create_label_image(text)
    label_img.save('final_label.png')
    conn = cups.Connection()
    conn.printFile(printer_name, 'final_label.png', "Label Print", {})
    os.remove('final_label.png')

def show_preview(image_path, on_print):
    preview = tk.Toplevel()
    preview.title("Label Preview")
    preview.geometry("1063x591")
    preview.resizable(False, False)
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(preview, image=img_tk)
    label.image = img_tk  # Keep reference
    label.pack()
    def print_and_close():
        on_print()
        preview.destroy()
    # Auto-close and print after 4 seconds (4000 ms)
    preview.after(4000, print_and_close)
    preview.grab_set()
    preview.wait_window()

def select_printer(printers):
    dialog = tk.Toplevel()
    dialog.title("Select Printer")
    dialog.geometry("400x250")  # Slightly larger for better visibility
    dialog.configure(bg="#f0f0f0")  # Match app background
    dialog.resizable(False, False)
    
    # Create a distinctive border
    frame = tk.Frame(dialog, bd=2, relief="ridge", bg="white", padx=20, pady=20)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tk.Label(frame, text="Select a printer:", font=("Arial", 14, "bold"), bg="white").pack(padx=10, pady=10)
    
    printer_var = tk.StringVar(value=printers[0] if printers else "")  # Default to first printer
    combo = ttk.Combobox(frame, textvariable=printer_var, values=printers, state="readonly", font=("Arial", 12))
    combo.pack(padx=10, pady=20, fill="x")
    
    button_frame = tk.Frame(frame, bg="white")
    button_frame.pack(pady=10, fill="x")
    
    selected = {'printer': None}
    
    def on_ok():
        selected['printer'] = printer_var.get()
        dialog.destroy()
    
    def on_cancel():
        dialog.destroy()
    
    # Auto-select timeout
    def auto_select():
        if not selected['printer'] and printers:
            selected['printer'] = printers[0]
            dialog.destroy()
    
    ok_btn = tk.Button(button_frame, text="OK", command=on_ok, font=("Arial", 12), 
                     bg="#4CAF50", fg="white", width=8)
    ok_btn.pack(side="left", padx=(50, 10))
    
    tk.Button(button_frame, text="Cancel", command=on_cancel, font=("Arial", 12),
             bg="#f44336", fg="white", width=8).pack(side="left")
    
    # Ensure dialog is on top and focused
    dialog.attributes('-topmost', True)
    dialog.update()
    dialog.attributes('-topmost', False)
    
    # Auto-select after 15 seconds if no choice made
    dialog.after(15000, auto_select)
    
    # Set focus to the OK button
    dialog.after(100, lambda: ok_btn.focus_set())
    
    dialog.grab_set()
    dialog.wait_window()
    
    # Return default printer if none selected
    if not selected['printer'] and printers:
        return printers[0]
        
    return selected['printer']

def show_auto_close_info(title, message, timeout=3000):
    info = tk.Toplevel()
    info.title(title)
    info.geometry("300x100")
    info.resizable(False, False)
    tk.Label(info, text=message, font=("Arial", 12)).pack(expand=True, padx=10, pady=10)
    info.after(timeout, info.destroy)
    info.grab_set()
    info.wait_window()

def load_printer_config():
    """Load the saved printer from configuration file"""
    try:
        if os.path.exists('printer_config.txt'):
            with open('printer_config.txt', 'r') as f:
                return f.read().strip()
    except Exception:
        pass
    return None

def get_saved_printer():
    """Get the saved printer from configuration"""
    saved_printer = load_printer_config()
    if saved_printer:
        # Verify printer still exists
        available_printers = get_printers()
        if saved_printer in available_printers:
            return saved_printer
    return None

# Replace your main() function with this
if __name__ == "__main__":
    app = LabelApp()
    app.mainloop()