import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
import barcode
from barcode.writer import ImageWriter
import cups
import os

def get_printers():
    conn = cups.Connection()
    return list(conn.getPrinters().keys())

def print_label(printer_name, text):
    # Generate barcode image
    CODE128 = barcode.get_barcode_class('code128')
    code = CODE128(text, writer=ImageWriter())
    filename = code.save('label_barcode')
    
    # Create label image with text and barcode
    barcode_img = Image.open(filename + '.png')
    label_img = Image.new('RGB', (barcode_img.width, barcode_img.height + 40), 'white')
    label_img.paste(barcode_img, (0, 0))
    
    # Add text below barcode
    from PIL import ImageDraw, ImageFont
    draw = ImageDraw.Draw(label_img)
    font = ImageFont.load_default()
    w, h = draw.textsize(text, font=font)
    draw.text(((barcode_img.width - w) // 2, barcode_img.height + 10), text, fill='black', font=font)
    
    label_img.save('final_label.png')
    
    # Print using CUPS
    conn = cups.Connection()
    conn.printFile(printer_name, 'final_label.png', "Label Print", {})
    os.remove(filename + '.png')
    os.remove('final_label.png')

def main():
    root = tk.Tk()
    root.withdraw()
    
    printers = get_printers()
    if not printers:
        messagebox.showerror("Error", "No printers found.")
        return
    
    printer = simpledialog.askstring("Printer", f"Available printers:\n{printers}\nEnter printer name:")
    if printer not in printers:
        messagebox.showerror("Error", "Invalid printer selected.")
        return
    
    text = simpledialog.askstring("Label Text", "Enter text for the label:")
    if not text:
        messagebox.showerror("Error", "No text entered.")
        return
    
    print_label(printer, text)
    messagebox.showinfo("Done", "Label sent to printer.")

if __name__ == "__main__":
    main()