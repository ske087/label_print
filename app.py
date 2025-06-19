import tkinter as tk
from tkinter import simpledialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import cups
import os

def get_printers():
    conn = cups.Connection()
    return list(conn.getPrinters().keys())

def create_label_image(text):
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
    tk.Label(dialog, text="Select a printer:").pack(padx=10, pady=5)
    printer_var = tk.StringVar()
    combo = ttk.Combobox(dialog, textvariable=printer_var, values=printers, state="readonly")
    combo.pack(padx=10, pady=5)
    combo.current(0)
    selected = {'printer': None}
    def on_ok():
        selected['printer'] = printer_var.get()
        dialog.destroy()
    btn = tk.Button(dialog, text="OK", command=on_ok)
    btn.pack(pady=10)
    dialog.grab_set()
    dialog.wait_window()
    return selected['printer']

def ask_label_text_with_preview():
    dialog = tk.Toplevel()
    dialog.title("Label Text")
    tk.Label(dialog, text="Enter text for the label:").pack(padx=10, pady=(10, 2))
    text_var = tk.StringVar()
    entry = tk.Entry(dialog, textvariable=text_var, width=40)
    entry.pack(padx=10, pady=2)
    preview_var = tk.BooleanVar(value=True)
    chk = tk.Checkbutton(dialog, text="Show print preview", variable=preview_var)
    chk.pack(padx=10, pady=2)
    result = {'text': None, 'preview': True}
    def on_ok():
        result['text'] = text_var.get()
        result['preview'] = preview_var.get()
        dialog.destroy()
    btn = tk.Button(dialog, text="OK", command=on_ok)
    btn.pack(pady=10)
    entry.focus()
    dialog.grab_set()
    dialog.wait_window()
    return result['text'], result['preview']

def show_auto_close_info(title, message, timeout=3000):
    info = tk.Toplevel()
    info.title(title)
    info.geometry("300x100")
    info.resizable(False, False)
    tk.Label(info, text=message, font=("Arial", 12)).pack(expand=True, padx=10, pady=10)
    info.after(timeout, info.destroy)
    info.grab_set()
    info.wait_window()

def main():
    root = tk.Tk()
    root.withdraw()
    
    printers = get_printers()
    if not printers:
        messagebox.showerror("Error", "No printers found.")
        return
    
    printer = select_printer(printers)
    if not printer:
        messagebox.showerror("Error", "No printer selected.")
        return
    
    text, do_preview = ask_label_text_with_preview()
    if not text:
        messagebox.showerror("Error", "No text entered.")
        return

    label_img = create_label_image(text)
    label_img.save('final_label.png')
    if do_preview:
        show_preview('final_label.png', lambda: print_label(printer, text))
        show_auto_close_info("Done", "Label sent to printer.", timeout=2000)
    else:
        print_label(printer, text)
        show_auto_close_info("Done", "Label sent to printer.", timeout=5000)

if __name__ == "__main__":
    main()