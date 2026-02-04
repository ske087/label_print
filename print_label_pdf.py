"""
PDF-based Label Printing Module
Generates high-quality PDF labels with barcodes for printing.
Uses reportlab for superior PDF generation compared to PNG rasterization.
Simplified layout: no borders, just field names and barcodes.
"""

from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from barcode import Code128
from barcode.writer import ImageWriter
import io
from PIL import Image
import os
import tempfile
import datetime


class PDFLabelGenerator:
    """Generate high-quality PDF labels with barcodes"""
    
    def __init__(self, label_width=11.5, label_height=8, dpi=300):
        """
        Initialize PDF label generator.
        
        Args:
            label_width (float): Width in cm (default 11.5 cm)
            label_height (float): Height in cm (default 8 cm)
            dpi (int): DPI for barcode generation (default 300 for print quality)
        """
        self.label_width = label_width * cm
        self.label_height = label_height * cm
        self.dpi = dpi
        self.margin = 3 * mm  # Minimal margin
    
    def generate_barcode_image(self, value, height_mm=18):
        """
        Generate barcode image from text value.
        
        Args:
            value (str): Text to encode in barcode (max 25 chars)
            height_mm (int): Barcode height in mm (default 18mm for 1.8cm)
            
        Returns:
            PIL.Image or None: Generated barcode image
        """
        if not value or not value.strip():
            return None
        
        try:
            # Truncate to 25 characters (Code128 limitation)
            value_truncated = value.strip()[:25]
            
            # Create barcode
            barcode_instance = Code128(value_truncated, writer=ImageWriter())
            
            # Generate in memory using a temporary directory
            temp_dir = tempfile.gettempdir()
            temp_name = f"barcode_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"
            temp_base_path = os.path.join(temp_dir, temp_name)
            
            # Barcode options - generate at high DPI for quality
            options = {
                'write_text': False,
                'module_width': 0.5,  # Width of each bar in mm
                'module_height': 8,  # Height in mm
                'quiet_zone': 2,
                'font_size': 0
            }
            
            barcode_instance.save(temp_base_path, options=options)
            
            # The barcode.save() adds .png extension automatically
            temp_path = temp_base_path + '.png'
            
            # Load and return image
            img = Image.open(temp_path)
            # Convert to RGB if needed
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Clean up temp file
            try:
                os.remove(temp_path)
            except:
                pass
            
            return img
        except Exception as e:
            # Log error but don't fail silently
            print(f"Barcode generation error for '{value}': {e}")
            return None
    
    def create_label_pdf(self, sap_nr, cantitate, lot_number, filename=None):
        """
        Create a PDF label with three rows of data and barcodes.
        Each row shows label name, barcode, and value text.
        
        Args:
            sap_nr (str): SAP article number
            cantitate (str): Quantity value
            lot_number (str): Lot/Cable ID
            filename (str): Output filename (if None, returns bytes)
            
        Returns:
            bytes or str: PDF content as bytes or filename if saved
        """
        # Prepare data for rows
        rows_data = [
            ("SAP-Nr", sap_nr),
            ("Cantitate", cantitate),
            ("Lot Nr", lot_number),
        ]
        
        # Create PDF canvas in memory or to file
        if filename:
            pdf_buffer = filename
        else:
            pdf_buffer = io.BytesIO()
        
        # Create canvas with label dimensions
        c = canvas.Canvas(pdf_buffer, pagesize=(self.label_width, self.label_height))
        
        # Calculate dimensions
        usable_width = self.label_width - 2 * self.margin
        row_height = (self.label_height - 2 * self.margin) / 3
        
        # Draw each row - label name, barcode, and value text
        for idx, (label_name, value) in enumerate(rows_data):
            y_position = self.label_height - self.margin - (idx + 1) * row_height
            
            # Draw label name (small, at top of row)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(
                self.margin,
                y_position + row_height - 3 * mm,
                label_name
            )
            
            # Generate and draw barcode if value exists
            if value and value.strip():
                barcode_value = value.strip()[:25]
                
                # Fixed barcode height: 1.6 cm (16mm) for optimal readability
                barcode_height_mm = 16
                barcode_height = barcode_height_mm * mm
                
                try:
                    barcode_img = self.generate_barcode_image(barcode_value, height_mm=barcode_height_mm)
                    
                    if barcode_img:
                        # Calculate barcode dimensions
                        max_barcode_width = usable_width - 2 * mm
                        aspect_ratio = barcode_img.width / barcode_img.height
                        barcode_width = barcode_height * aspect_ratio
                        
                        # Constrain width to fit in label
                        if barcode_width > max_barcode_width:
                            barcode_width = max_barcode_width
                        
                        # Save barcode temporarily and draw on PDF
                        barcode_temp = tempfile.NamedTemporaryFile(suffix='.png', delete=False)
                        barcode_path = barcode_temp.name
                        barcode_temp.close()
                        
                        barcode_img.save(barcode_path, 'PNG')
                        
                        # Position barcode vertically centered in middle of row
                        barcode_y = y_position + (row_height - barcode_height) / 2
                        
                        # Draw barcode image
                        c.drawImage(
                            barcode_path,
                            self.margin,
                            barcode_y,
                            width=barcode_width,
                            height=barcode_height,
                            preserveAspectRatio=True
                        )
                        
                        # Draw small text below barcode showing the value
                        c.setFont("Helvetica", 6)
                        c.drawString(
                            self.margin,
                            barcode_y - 3 * mm,
                            f"({barcode_value})"
                        )
                        
                        # Clean up
                        try:
                            os.remove(barcode_path)
                        except:
                            pass
                    else:
                        # If barcode generation failed, show text
                        c.setFont("Helvetica", 10)
                        c.drawString(
                            self.margin,
                            y_position + row_height / 2,
                            f"[No Barcode: {barcode_value}]"
                        )
                except Exception as e:
                    # Fallback: draw value as text with error indicator
                    print(f"PDF barcode error: {e}")
                    c.setFont("Helvetica", 10)
                    c.drawString(
                        self.margin,
                        y_position + row_height / 2,
                        f"[Text: {barcode_value}]"
                    )
            else:
                # Empty value - show placeholder
                c.setFont("Helvetica", 8)
                c.drawString(
                    self.margin,
                    y_position + row_height / 2,
                    "(empty)"
                )
        
        # Save PDF
        c.save()
        
        # Return filename or bytes
        if filename:
            return filename
        else:
            pdf_buffer.seek(0)
            return pdf_buffer.getvalue()
    
    def create_label_pdf_file(self, sap_nr, cantitate, lot_number, filename=None):
        """
        Create PDF label file and return the filename.
        
        Args:
            sap_nr (str): SAP article number
            cantitate (str): Quantity value
            lot_number (str): Lot/Cable ID
            filename (str): Output filename (if None, auto-generates)
            
        Returns:
            str: Path to created PDF file
        """
        if not filename:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"label_{timestamp}.pdf"
        
        return self.create_label_pdf(sap_nr, cantitate, lot_number, filename)


def create_label_pdf_simple(text):
    """
    Simple wrapper to create PDF from combined text (SAP|CANTITATE|LOT).
    
    Args:
        text (str): Combined text in format "SAP|CANTITATE|LOT"
        
    Returns:
        bytes: PDF content
    """
    # Parse text
    parts = text.split('|') if '|' in text else [text, '', '']
    sap_nr = parts[0].strip() if len(parts) > 0 else ''
    cantitate = parts[1].strip() if len(parts) > 1 else ''
    lot_number = parts[2].strip() if len(parts) > 2 else ''
    
    generator = PDFLabelGenerator()
    pdf_bytes = generator.create_label_pdf(sap_nr, cantitate, lot_number)
    
    return pdf_bytes


def create_label_pdf_file(text, filename=None):
    """
    Create PDF label file from combined text.
    
    Args:
        text (str): Combined text in format "SAP|CANTITATE|LOT"
        filename (str): Output filename (auto-generates if None)
        
    Returns:
        str: Path to created PDF file
    """
    # Parse text
    parts = text.split('|') if '|' in text else [text, '', '']
    sap_nr = parts[0].strip() if len(parts) > 0 else ''
    cantitate = parts[1].strip() if len(parts) > 1 else ''
    lot_number = parts[2].strip() if len(parts) > 2 else ''
    
    if not filename:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"label_{timestamp}.pdf"
    
    generator = PDFLabelGenerator()
    return generator.create_label_pdf(sap_nr, cantitate, lot_number, filename)
