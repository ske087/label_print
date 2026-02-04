#!/usr/bin/env python3
"""
Test Label Printer - Non-GUI Tests
Tests printing functionality without GUI/graphics
"""

import os
import sys

def test_module_imports():
    """Test that all required modules can be imported"""
    print("=" * 60)
    print("TEST 1: Module Imports")
    print("=" * 60)
    
    modules = {
        'PIL': 'Image processing',
        'barcode': 'Barcode generation',
        'cups': 'Printer interface',
        'print_label': 'Label printing module'
    }
    
    all_ok = True
    for module, description in modules.items():
        try:
            __import__(module)
            print(f"✓ {module:<20} - {description}")
        except ImportError as e:
            print(f"✗ {module:<20} - FAILED: {e}")
            all_ok = False
    
    return all_ok

def test_label_generation():
    """Test label image generation"""
    print("\n" + "=" * 60)
    print("TEST 2: Label Image Generation")
    print("=" * 60)
    
    try:
        from print_label import create_label_image
        
        test_cases = [
            "SAP123",
            "SAP456|100",
            "SAP789|50|REEL001"
        ]
        
        for test_text in test_cases:
            image = create_label_image(test_text)
            print(f"✓ Generated label for: '{test_text}' - Size: {image.size}")
        
        return True
    except Exception as e:
        print(f"✗ Label generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_printer_detection():
    """Test printer detection"""
    print("\n" + "=" * 60)
    print("TEST 3: Printer Detection")
    print("=" * 60)
    
    try:
        import cups
        
        conn = cups.Connection()
        printers = conn.getPrinters()
        
        if printers:
            print(f"✓ Found {len(printers)} printer(s):")
            for name, details in list(printers.items())[:5]:
                status = details.get('printer-state', 'unknown')
                print(f"  - {name:<30} (State: {status})")
        else:
            print("⚠ No printers configured (will use PDF)")
        
        return True
    except Exception as e:
        print(f"✗ Printer detection failed: {e}")
        return False

def test_save_label():
    """Test saving label to file"""
    print("\n" + "=" * 60)
    print("TEST 4: Save Label to File")
    print("=" * 60)
    
    try:
        from print_label import create_label_image
        import tempfile
        
        # Create test label
        test_text = "TEST_LABEL|123|REEL"
        image = create_label_image(test_text)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
            image.save(tmp.name)
            tmp_path = tmp.name
        
        # Check if file exists and has content
        file_size = os.path.getsize(tmp_path)
        print(f"✓ Label saved successfully")
        print(f"  - File: {tmp_path}")
        print(f"  - Size: {file_size:,} bytes")
        
        # Clean up
        os.remove(tmp_path)
        print(f"  - Cleaned up temporary file")
        
        return True
    except Exception as e:
        print(f"✗ Save label test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_formats():
    """Test different data format combinations"""
    print("\n" + "=" * 60)
    print("TEST 5: Data Format Testing")
    print("=" * 60)
    
    try:
        from print_label import create_label_image
        
        test_formats = [
            ("A012345", "SAP only"),
            ("A012345|50", "SAP + Quantity"),
            ("A012345|50|REEL001", "SAP + Quantity + Cable ID"),
            ("SPEC-123|999|CABLE-X", "Complex format"),
            ("123456789012345678901234567890", "Long string"),
        ]
        
        for data, description in test_formats:
            try:
                image = create_label_image(data)
                print(f"✓ {description:<30} - OK")
            except Exception as e:
                print(f"✗ {description:<30} - FAILED: {e}")
                return False
        
        return True
    except Exception as e:
        print(f"✗ Data format test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  LABEL PRINTER - FUNCTIONAL TESTS".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    tests = [
        ("Module Imports", test_module_imports),
        ("Label Generation", test_label_generation),
        ("Printer Detection", test_printer_detection),
        ("Save Label to File", test_save_label),
        ("Data Format Testing", test_data_formats),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n✗ Test '{test_name}' crashed: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    print()
    
    if passed == total:
        print("✓ ALL TESTS PASSED! System is ready to use.")
        print("\nNext steps:")
        print("  1. Fix graphics driver issue for GUI display")
        print("  2. Or use the printing API directly in your code")
        return 0
    else:
        print("✗ Some tests failed. Please review the output above.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
