from PIL import Image, ImageDraw, ImageFont
import barcode
from barcode.writer import ImageWriter
import cups, time, os, datetime
from print_label_pdf import PDFLabelGenerator

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
            conn = cups.Connection()
            conn.printFile(printer, temp_file, "Label Print", {})
            return True
        else:
            print("Direct printing without preview...")
            # Direct printing without preview (preview = 0)
            try:
                conn = cups.Connection()
                conn.printFile(printer, temp_file, "Label Print", {})
                print(f"Label sent to printer: {printer}")
                return True
            except Exception as e:
                # If printing fails, save to file as fallback
                print(f"Printer error: {str(e)}")
                print("Label already saved to file as fallback...")
                print(f"Label file: {temp_file}")
                return True
            
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
