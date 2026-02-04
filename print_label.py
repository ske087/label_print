from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import time
import os
import datetime
import platform
import subprocess
from print_label_pdf import PDFLabelGenerator

# Cross-platform printer support
try:
    import cups
    CUPS_AVAILABLE = True
except ImportError:
    CUPS_AVAILABLE = False

try:
    import win32api
    import win32print
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

SYSTEM = platform.system()  # 'Linux', 'Windows', 'Darwin'


def get_available_printers():
    """
    Get list of available printers (cross-platform).
    
    Returns:
        list: List of available printer names, with "PDF" as fallback
    """
    try:
        if SYSTEM == "Linux" and CUPS_AVAILABLE:
            # Linux: Use CUPS
            conn = cups.Connection()
            printers = conn.getPrinters()
            return list(printers.keys()) if printers else ["PDF"]
        
        elif SYSTEM == "Windows":
            # Windows: Try win32print first
            try:
                printers = []
                for printer_name in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL):
                    printers.append(printer_name[2])
                return printers if printers else ["PDF"]
            except:
                # Fallback for Windows if win32print fails
                return ["PDF"]
        
        elif SYSTEM == "Darwin":
            # macOS: Use lpstat command
            try:
                result = subprocess.run(["lpstat", "-p", "-d"], 
                                      capture_output=True, text=True)
                printers = []
                for line in result.stdout.split('\n'):
                    if line.startswith('printer'):
                        printer_name = line.split()[1]
                        printers.append(printer_name)
                return printers if printers else ["PDF"]
            except:
                return ["PDF"]
        
        else:
            return ["PDF"]
    
    except Exception as e:
        print(f"Error getting printers: {e}")
        return ["PDF"]


def create_label_image(text):
    """
    Create a label image with 3 rows: label + barcode for each field.
    
    Args:
        text (str): Combined text in format "SAP|CANTITATE|LOT" or single value
        
    Returns:
        PIL.Image: The generated label image
    """
    # Parse the text input
    parts = text.split('|') if '|' in text else [text, '', '']
    sap_nr = parts[0].strip() if len(parts) > 0 else ''
    cantitate = parts[1].strip() if len(parts) > 1 else ''
    lot_number = parts[2].strip() if len(parts) > 2 else ''
    
    # Label dimensions (narrower, 3 rows)
    label_width = 800   # 8 cm
    label_height = 600  # 6 cm
    
    # Create canvas
    label_img = Image.new('RGB', (label_width, label_height), 'white')
    draw = ImageDraw.Draw(label_img)
    
    # Row setup - 3 equal rows
    row_height = label_height // 3
    left_margin = 15
    row_spacing = 3
    
    # Fonts
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    try:
        label_font = ImageFont.truetype(font_path, 16)
        value_font = ImageFont.truetype(font_path, 14)
    except IOError:
        label_font = ImageFont.load_default()
        value_font = ImageFont.load_default()
    
    # Data for 3 rows
    rows_data = [
        ("SAP-Nr", sap_nr),
        ("Cantitate", cantitate),
        ("Lot Nr", lot_number),
    ]
    
    # Generate barcodes first
    CODE128 = barcode.get_barcode_class('code128')
    writer_options = {
        "write_text": False,
        "module_width": 0.4,
        "module_height": 8,
        "quiet_zone": 2,
        "font_size": 0
    }
    
    barcode_images = []
    for _, value in rows_data:
        if value:
            try:
                code = CODE128(value[:25], writer=ImageWriter())
                filename = code.save('temp_barcode', options=writer_options)
                barcode_img = Image.open(filename)
                barcode_images.append(barcode_img)
            except:
                barcode_images.append(None)
        else:
            barcode_images.append(None)
    
    # Draw each row with label and barcode
    for idx, ((label_name, value), barcode_img) in enumerate(zip(rows_data, barcode_images)):
        row_y = idx * row_height
        
        # Draw label name
        draw.text(
            (left_margin, row_y + 3),
            label_name,
            fill='black',
            font=label_font
        )
        
        # Draw barcode if available
        if barcode_img:
            # Resize barcode to fit in row width
            barcode_width = label_width - left_margin - 10
            barcode_height = row_height - 25
            barcode_resized = barcode_img.resize((barcode_width, barcode_height), Image.LANCZOS)
            label_img.paste(barcode_resized, (left_margin, row_y + 20))
        else:
            # Fallback: show value as text
            draw.text(
                (left_margin, row_y + 25),
                value if value else "(empty)",
                fill='black',
                font=value_font
            )
    
    # Clean up temporary barcode files
    try:
        if os.path.exists('temp_barcode.png'):
            os.remove('temp_barcode.png')
    except:
        pass
    
    return label_img


def create_label_pdf(text):
    """
    Create a high-quality PDF label with 3 rows: label + barcode for each field.
    PDFs are saved to the pdf_backup folder.
    
    Args:
        text (str): Combined text in format "SAP|CANTITATE|LOT" or single value
        
    Returns:
        str: Path to the generated PDF file
    """
    # Parse the text input
    parts = text.split('|') if '|' in text else [text, '', '']
    sap_nr = parts[0].strip() if len(parts) > 0 else ''
    cantitate = parts[1].strip() if len(parts) > 1 else ''
    lot_number = parts[2].strip() if len(parts) > 2 else ''
    
    # Create PDF using high-quality generator
    generator = PDFLabelGenerator()
    
    # Ensure pdf_backup folder exists
    pdf_backup_dir = 'pdf_backup'
    os.makedirs(pdf_backup_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = os.path.join(pdf_backup_dir, f"final_label_{timestamp}.pdf")
    
    return generator.create_label_pdf(sap_nr, cantitate, lot_number, pdf_filename)


def print_to_printer(printer_name, file_path):
    """
    Print file to printer (cross-platform).
    
    Args:
        printer_name (str): Name of printer or "PDF" for PDF output
        file_path (str): Path to file to print
        
    Returns:
        bool: True if successful
    """
    try:
        if printer_name == "PDF":
            # PDF output - file is already saved
            print(f"PDF output: {file_path}")
            return True
        
        elif SYSTEM == "Linux" and CUPS_AVAILABLE:
            # Linux: Use CUPS
            conn = cups.Connection()
            conn.printFile(printer_name, file_path, "Label Print", {})
            print(f"Label sent to printer: {printer_name}")
            return True
        
        elif SYSTEM == "Windows":
            # Windows: Use win32print or open with default printer
            try:
                if WIN32_AVAILABLE:
                    import win32print
                    import win32api
                    # Print using the Windows API
                    win32api.ShellExecute(0, "print", file_path, f'/d:"{printer_name}"', ".", 0)
                    print(f"Label sent to printer: {printer_name}")
                    return True
                else:
                    # Fallback: Open with default printer
                    if file_path.endswith('.pdf'):
                        os.startfile(file_path, "print")
                    else:
                        # For images, use default print application
                        subprocess.run([f'notepad', '/p', file_path], check=False)
                    print(f"Label sent to default printer")
                    return True
            except Exception as e:
                print(f"Windows print error: {e}")
                print("PDF backup saved as fallback")
                return True
        
        elif SYSTEM == "Darwin":
            # macOS: Use lp command
            subprocess.run(["lp", "-d", printer_name, file_path], check=True)
            print(f"Label sent to printer: {printer_name}")
            return True
        
        else:
            print(f"Unsupported system: {SYSTEM}")
            return False
    
    except Exception as e:
        print(f"Printer error: {str(e)}")
        print("Label already saved to file as fallback...")
        print(f"Label file: {file_path}")
        return True


def print_label_standalone(value, printer, preview=0, use_pdf=True):
    """
    Print a label with the specified text on the specified printer.
    
    Args:
        value (str): The text to print on the label
        printer (str): The name of the printer to use
        preview (int): 0 = no preview, 1-3 = 3s preview, >3 = 5s preview
        use_pdf (bool): True to use PDF (recommended for quality), False for PNG
    
    Returns:
        bool: True if printing was successful, False otherwise
    """
    # For tracking if file was created
    file_created = False
    temp_file = None
    
    try:
        # Debug output
        print(f"Preview value: {preview}")
        print(f"Preview type: {type(preview)}")
        print(f"Using format: {'PDF' if use_pdf else 'PNG'}")
        
        # Create label in selected format
        if use_pdf:
            temp_file = create_label_pdf(value)
            print(f"PDF label created: {temp_file}")
            print(f"PDF backup saved to: {temp_file}")
        else:
            # Create the label image (PNG)
            label_img = create_label_image(value)
            temp_file = 'final_label.png'
            label_img.save(temp_file)
            print(f"PNG label created: {temp_file}")
        
        file_created = True
        
        # Convert preview to int if it's a string
        if isinstance(preview, str):
            preview = int(preview)
        
        if preview > 0:  # Any value above 0 shows a preview message
            # Calculate preview duration in seconds
            if 1 <= preview <= 3:
                preview_sec = 3  # 3 seconds
            else:  # preview > 3
                preview_sec = 5  # 5 seconds
            
            print(f"Printing in {preview_sec} seconds... (Press Ctrl+C to cancel)")
            
            # Simple countdown timer using time.sleep
            try:
                for i in range(preview_sec, 0, -1):
                    print(f"  {i}...", end=" ", flush=True)
                    time.sleep(1)
                print("\nPrinting now...")
            except KeyboardInterrupt:
                print("\nCancelled by user")
                return False
            
            # Print after preview
            print("Sending to printer...")
            return print_to_printer(printer, temp_file)
        else:
            print("Direct printing without preview...")
            # Direct printing without preview (preview = 0)
            return print_to_printer(printer, temp_file)
            
    except Exception as e:
        print(f"Error printing label: {str(e)}")
        return False
        
    finally:
        # This block always executes, ensuring cleanup
        if use_pdf:
            print(f"Cleanup complete - PDF backup saved to pdf_backup folder")
        else:
            print("Cleanup complete - label file retained for reference")


# Main code removed - import this module or run as part of the Kivy GUI application
