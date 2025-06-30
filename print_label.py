from PIL import Image, ImageTk, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import cups, time, os
import tkinter as tk  # Add this explicitly at the top

#functie de printare etichete pe un printer specificat cu un preview opțional
# Aceasta funcție creează o imagine cu un cod de bare și text, apoi o trimite la imprimantă.
# Dacă este specificat un preview, afișează o fereastră de previzualizare înainte de a imprima.
# Dimensiunea etichetei este de 9x5 cm la 300 DPI, cu un cadru exterior și două cadre interioare pentru codul de bare și text.
# Codul de bare este generat folosind formatul Code128, iar textul este afișat sub codul de bare cu
# o dimensiune de font maximizată pentru a se potrivi în cadrul textului
# Imaginile sunt create folosind biblioteca PIL, iar imprimarea se face prin intermediul
# bibliotecii CUPS pentru gestionarea imprimantelor.
# Această funcție este utilă pentru a crea etichete personalizate cu coduri de bare și text, care pot fi utilizate în diverse aplicații, cum ar fi etichetarea produselor, inventariere sau organizarea documentelor
#mod de utilizare in cadrul unui program se copie fisierul print_label.py in directorul de lucru
# si se apeleaza functia print_label_standalone cu parametrii corespunzători:
# - value: textul de afișat pe etichetă
# - printer: numele imprimantei pe care se va face printarea
# - preview: 0 pentru a nu afișa previzualizarea, 1-3 pentru o previzualizare de 3 secunde, >3 pentru o previzualizare de 5 secunde 

# se recomanda instalarea si setarea imprimantei in sistemul de operare
# pentru a putea fi utilizata de catre biblioteca CUPS 
# se verifica proprietatile imprimantei in cups sa fie setata dimensiunea corecta a etichetei
# pentru a instala biblioteca barcode se foloseste comanda pip install python-barcode
# pentru a instala biblioteca PIL se foloseste comanda pip install pillow
# pentru a instala biblioteca CUPS se foloseste comanda pip install pycups
# pentru a instala biblioteca Tkinter se foloseste comanda sudo apt-get install python3-tk


def create_label_image(text):
    """
    Create a label image with barcode and text.
    
    Args:
        text (str): The text to encode in the barcode and display
        
    Returns:
        PIL.Image: The generated label image
    """
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

    os.remove(filename)  # Clean up temporary barcode file
    return label_img

def print_label_standalone(value, printer, preview=0):
    """
    Print a label with the specified text on the specified printer.
    
    Args:
        value (str): The text to print on the label
        printer (str): The name of the printer to use
        preview (int): 0 = no preview, 1-3 = 3s preview, >3 = 5s preview
    
    Returns:
        bool: True if printing was successful, False otherwise
    """
    # For tracking if file was created
    file_created = False
    
    try:
        # Debug output
        print(f"Preview value: {preview}")
        print(f"Preview type: {type(preview)}")
        
        # Create the label image
        label_img = create_label_image(value)
        label_img.save('final_label.png')
        file_created = True
        
        # Convert preview to int if it's a string
        if isinstance(preview, str):
            preview = int(preview)
        
        if preview > 0:  # Any value above 0 shows a preview
            print("Showing preview window...")
            # Calculate preview duration in milliseconds
            if 1 <= preview <= 3:
                preview_ms = 3000  # 3 seconds
            else:  # preview > 3
                preview_ms = 5000  # 5 seconds
                
            # Create a Tkinter window for preview - simpler approach
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            preview_window = tk.Toplevel(root)
            preview_window.title("Label Preview")
            preview_window.geometry("1063x691")  # A bit taller to accommodate buttons
            
            # Track if printing was done
            printed = False
            
            # Function to print and close the preview
            def do_print():
                nonlocal printed
                print("Printing from preview...")
                conn = cups.Connection()
                conn.printFile(printer, 'final_label.png', "Label Print", {})
                printed = True
                preview_window.destroy()
                root.quit()  # Important! This ensures mainloop exits
            
            # Function to close without printing
            def do_cancel():
                preview_window.destroy()
                root.quit()  # Important! This ensures mainloop exits
            
            # Display the image
            img = Image.open('final_label.png')
            img_tk = ImageTk.PhotoImage(img)
            label = tk.Label(preview_window, image=img_tk)
            label.image = img_tk  # Keep reference
            label.pack(pady=10)
            
            # Add a timer label
            timer_text = f"Auto-printing in {preview_ms//1000} seconds..."
            timer_label = tk.Label(preview_window, text=timer_text, font=("Arial", 10))
            timer_label.pack(pady=(0, 5))
            
            # Button frame
            btn_frame = tk.Frame(preview_window)
            btn_frame.pack(pady=10)
            
            # Add print and cancel buttons
            print_btn = tk.Button(btn_frame, text="Print Now", command=do_print, 
                                font=("Arial", 12), bg="#4CAF50", fg="white", padx=20, pady=5)
            print_btn.pack(side="left", padx=10)
            
            cancel_btn = tk.Button(btn_frame, text="Cancel", command=do_cancel, 
                                font=("Arial", 12), bg="#f44336", fg="white", padx=20, pady=5)
            cancel_btn.pack(side="left", padx=10)
            
            # Auto-print after the specified time
            print(f"Setting auto-print timer for {preview_ms}ms")
            preview_window.after(preview_ms, do_print)
            
            # Make sure the window stays on top
            preview_window.attributes('-topmost', True)
            preview_window.update()
            preview_window.attributes('-topmost', False)
            
            # Wait for the window to close
            root.mainloop()
            
            if not printed:
                print("User cancelled printing")
                return False
                
            return True
        else:
            print("Direct printing without preview...")
            # Direct printing without preview (preview = 0)
            conn = cups.Connection()
            conn.printFile(printer, 'final_label.png', "Label Print", {})
            return True
            
    except Exception as e:
        print(f"Error printing label: {str(e)}")
        return False
        
    finally:
        # This block always executes, ensuring cleanup
        print("Cleaning up temporary files...")
        if file_created and os.path.exists('final_label.png'):
            try:
                os.remove('final_label.png')
                print("Cleanup successful")
            except Exception as e:
                print(f"Warning: Could not remove temporary file: {str(e)}")

value = "A012345"
printer = "PDF"
preview = 3  # Set preview duration (0 = no preview, 1-3 = 3s, >3 = 5s)
print_label_standalone(value, printer, preview)
