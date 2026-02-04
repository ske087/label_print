#!/usr/bin/env python3
"""
Demo: PDF Label Generation System
Shows how to use the new PDF-based label printing system
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

from print_label_pdf import PDFLabelGenerator, create_label_pdf_file
from print_label import print_label_standalone, create_label_pdf


def demo_basic_pdf_generation():
    """Demo 1: Basic PDF generation"""
    print("=" * 60)
    print("DEMO 1: Basic PDF Label Generation")
    print("=" * 60)
    
    # Create a simple label
    pdf_file = create_label_pdf_file(
        text="SAP-12345|Qty:100|LOT-ABC",
        filename="demo_label_basic.pdf"
    )
    
    print(f"✓ Generated: {pdf_file}")
    print(f"✓ File size: {os.path.getsize(pdf_file)} bytes")
    print()


def demo_custom_dimensions():
    """Demo 2: Custom label dimensions"""
    print("=" * 60)
    print("DEMO 2: Custom Label Dimensions")
    print("=" * 60)
    
    # Create generator with custom size (smaller label)
    generator = PDFLabelGenerator(label_width=6, label_height=4, dpi=300)
    
    pdf_file = generator.create_label_pdf(
        sap_nr="SAP-67890",
        cantitate="Qty:250",
        lot_number="LOT-XYZ",
        filename="demo_label_custom.pdf"
    )
    
    print(f"✓ Custom 6cm × 4cm label generated")
    print(f"✓ File: {pdf_file}")
    print(f"✓ File size: {os.path.getsize(pdf_file)} bytes")
    print()


def demo_batch_generation():
    """Demo 3: Batch label generation"""
    print("=" * 60)
    print("DEMO 3: Batch Label Generation")
    print("=" * 60)
    
    labels_data = [
        ("SAP-001", "Qty:100", "LOT-A"),
        ("SAP-002", "Qty:200", "LOT-B"),
        ("SAP-003", "Qty:300", "LOT-C"),
        ("SAP-004", "Qty:150", "LOT-D"),
    ]
    
    generator = PDFLabelGenerator()
    generated_files = []
    
    for idx, (sap, qty, lot) in enumerate(labels_data, 1):
        pdf_file = generator.create_label_pdf(
            sap_nr=sap,
            cantitate=qty,
            lot_number=lot,
            filename=f"demo_batch_label_{idx:02d}.pdf"
        )
        generated_files.append(pdf_file)
        print(f"  [{idx}] Generated {pdf_file}")
    
    total_size = sum(os.path.getsize(f) for f in generated_files)
    print(f"\n✓ Total: {len(generated_files)} labels generated")
    print(f"✓ Combined size: {total_size} bytes")
    print()


def demo_high_dpi():
    """Demo 4: High DPI for ultra-quality printing"""
    print("=" * 60)
    print("DEMO 4: High DPI Generation (600 DPI)")
    print("=" * 60)
    
    # Create generator with higher DPI for premium printing
    generator = PDFLabelGenerator(label_width=8.5, label_height=6, dpi=600)
    
    pdf_file = generator.create_label_pdf(
        sap_nr="SAP-PREMIUM",
        cantitate="Qty:500",
        lot_number="LOT-PREMIUM",
        filename="demo_label_600dpi.pdf"
    )
    
    print(f"✓ 600 DPI Ultra-quality label generated")
    print(f"✓ File: {pdf_file}")
    print(f"✓ File size: {os.path.getsize(pdf_file)} bytes")
    print(f"✓ Use this for color-critical or high-volume production")
    print()


def demo_api_usage():
    """Demo 5: Using the convenience API"""
    print("=" * 60)
    print("DEMO 5: Convenience API Usage")
    print("=" * 60)
    
    # Method 1: Simple function
    print("Method 1: Using print_label_standalone()")
    print("  Usage: print_label_standalone(text, printer, preview=0, use_pdf=True)")
    print()
    
    # Method 2: Direct PDF creation
    print("Method 2: Using create_label_pdf()")
    pdf_file = create_label_pdf("SAP-TEST|Qty:999|LOT-TEST")
    print(f"  ✓ Generated: {pdf_file}")
    print()
    
    # Method 3: Generator class
    print("Method 3: Using PDFLabelGenerator class")
    print("  Usage:")
    print("    generator = PDFLabelGenerator()")
    print("    pdf = generator.create_label_pdf(sap_nr, qty, lot, filename)")
    print()


def demo_comparison():
    """Demo 6: PNG vs PDF comparison"""
    print("=" * 60)
    print("DEMO 6: PNG vs PDF Comparison")
    print("=" * 60)
    
    from print_label import create_label_image
    
    # Generate PNG
    png_img = create_label_image("SAP-CMP|Qty:100|LOT-CMP")
    png_file = "demo_comparison_png.png"
    png_img.save(png_file)
    png_size = os.path.getsize(png_file)
    
    # Generate PDF
    pdf_file = create_label_pdf_file("SAP-CMP|Qty:100|LOT-CMP", "demo_comparison_pdf.pdf")
    pdf_size = os.path.getsize(pdf_file)
    
    print("File Size Comparison:")
    print(f"  PNG: {png_size:,} bytes")
    print(f"  PDF: {pdf_size:,} bytes")
    print(f"  Savings: {png_size - pdf_size:,} bytes ({((png_size-pdf_size)/png_size)*100:.1f}%)")
    print()
    
    print("Quality Comparison:")
    print("  PNG:  Rasterized, fixed resolution")
    print("  PDF:  Vector-based, infinite scalability")
    print()
    
    print("Recommended Use:")
    print("  ✓ Use PDF for production printing (recommended)")
    print("  ✓ Use PNG for legacy systems or special cases")
    print()


def cleanup_demo_files():
    """Clean up generated demo files"""
    print("=" * 60)
    print("Cleaning up demo files...")
    print("=" * 60)
    
    demo_files = [
        "demo_label_basic.pdf",
        "demo_label_custom.pdf",
        "demo_batch_label_01.pdf",
        "demo_batch_label_02.pdf",
        "demo_batch_label_03.pdf",
        "demo_batch_label_04.pdf",
        "demo_label_600dpi.pdf",
        "demo_comparison_png.png",
        "demo_comparison_pdf.pdf",
    ]
    
    for filename in demo_files:
        if os.path.exists(filename):
            os.remove(filename)
            print(f"  ✓ Removed {filename}")
    
    print("\n✓ Cleanup complete")
    print()


if __name__ == "__main__":
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  PDF Label Generation System - Comprehensive Demo".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    print("\n")
    
    try:
        # Run all demos
        demo_basic_pdf_generation()
        demo_custom_dimensions()
        demo_batch_generation()
        demo_high_dpi()
        demo_api_usage()
        demo_comparison()
        
        # Ask about cleanup
        print("\nDo you want to clean up demo files? (y/n): ", end="")
        # For automated testing, auto-cleanup
        cleanup_demo_files()
        
        print("\n" + "=" * 60)
        print("✓ All demos completed successfully!")
        print("=" * 60)
        print("\nKey Takeaways:")
        print("  1. PDF generation is the recommended format for printing")
        print("  2. Supports custom dimensions and DPI settings")
        print("  3. File sizes are comparable to PNG with better quality")
        print("  4. Batch processing is simple and efficient")
        print("  5. Full backward compatibility with PNG option")
        print("\nFor more information, see PDF_UPGRADE_GUIDE.md")
        print()
        
    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
