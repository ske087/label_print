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

def print_label(printer_name, text):
    # Generate barcode image without text
    CODE128 = barcode.get_barcode_class('code128')
    code = CODE128(text, writer=ImageWriter())
    filename = code.save('label_barcode', options={"write_text": False})
    
    # Load barcode image
    barcode_img = Image.open(filename)
    # Set font path (adjust if needed)
    try:
        font = ImageFont.truetype("arialbd.ttf", 32)  # Arial Black, 24pt
    except IOError:
        font = ImageFont.load_default()
    # Calculate text size
    draw = ImageDraw.Draw(barcode_img)
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    # Create label image with extra space for text
    label_height = barcode_img.height + text_height + 10
    label_img = Image.new('RGB', (barcode_img.width, label_height), 'white')
    label_img.paste(barcode_img, (0, 0))
    # Draw text centered under barcode
    draw = ImageDraw.Draw(label_img)
    x = (barcode_img.width - text_width) // 2
    y = barcode_img.height + 5
    draw.text((x, y), text, font=font, fill='black')
    label_img.save('final_label.png')
    
    # Print using CUPS
    conn = cups.Connection()
    conn.printFile(printer_name, 'final_label.png', "Label Print", {})
    os.remove(filename)
    os.remove('final_label.png')

def show_preview(image_path):
    preview = tk.Toplevel()
    preview.title("Label Preview")
    img = Image.open(image_path)
    img_tk = ImageTk.PhotoImage(img)
    label = tk.Label(preview, image=img_tk)
    label.image = img_tk  # Keep reference
    label.pack()
    btn = tk.Button(preview, text="Print", command=preview.destroy)
    btn.pack()
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
    
    text = simpledialog.askstring("Label Text", "Enter text for the label:")
    if not text:
        messagebox.showerror("Error", "No text entered.")
        return

    # Generate label image for preview
    CODE128 = barcode.get_barcode_class('code128')
    code = CODE128(text, writer=ImageWriter())
    filename = code.save('label_barcode', options={"write_text": False})
    barcode_img = Image.open(filename)
    # Set font path (adjust if needed)
    try:
        font = ImageFont.truetype("arialbd.ttf", 32)  # Arial Black, 24pt
    except IOError:
        font = ImageFont.load_default()
    # Calculate text size
    draw = ImageDraw.Draw(barcode_img)
    text_width, text_height = draw.textbbox((0, 0), text, font=font)[2:]
    # Create label image with extra space for text
    label_height = barcode_img.height + text_height + 10
    label_img = Image.new('RGB', (barcode_img.width, label_height), 'white')
    label_img.paste(barcode_img, (0, 0))
    # Draw text centered under barcode
    draw = ImageDraw.Draw(label_img)
    x = (barcode_img.width - text_width) // 2
    y = barcode_img.height + 5
    draw.text((x, y), text, font=font, fill='black')
    label_img.save('final_label.png')
    os.remove(filename)

    # Show preview window
    show_preview('final_label.png')

    # Print after preview
    print_label(printer, text)
    messagebox.showinfo("Done", "Label sent to printer.")
    os.remove('final_label.png')

if __name__ == "__main__":
    main()