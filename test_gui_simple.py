#!/usr/bin/env python3
"""
Simple test to verify GUI components work
"""

print("Testing Label Printer GUI components...")
print()

# Test 1: Import modules
print("[1/5] Testing imports...")
try:
    from kivy.app import App
    from kivy.uix.boxlayout import BoxLayout
    from kivy.uix.label import Label
    from kivy.uix.textinput import TextInput
    from kivy.uix.button import Button
    print("✓ Kivy imports successful")
except Exception as e:
    print(f"✗ Kivy import failed: {e}")
    exit(1)

# Test 2: Import printing modules
print()
print("[2/5] Testing printing module...")
try:
    from print_label import create_label_image, print_label_standalone
    print("✓ Printing module imports successful")
except Exception as e:
    print(f"✗ Printing module import failed: {e}")
    exit(1)

# Test 3: Test label image generation
print()
print("[3/5] Testing label image generation...")
try:
    test_text = "TEST|123|REEL001"
    image = create_label_image(test_text)
    print(f"✓ Label image created: {image.size}")
except Exception as e:
    print(f"✗ Label image generation failed: {e}")
    exit(1)

# Test 4: Test printer detection
print()
print("[4/5] Testing printer detection...")
try:
    import cups
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_list = list(printers.keys()) if printers else []
    if printer_list:
        print(f"✓ Printers found: {', '.join(printer_list[:3])}")
    else:
        print("⚠ No printers found (will use PDF)")
except Exception as e:
    print(f"✗ Printer detection failed: {e}")

# Test 5: Create simple test app
print()
print("[5/5] Creating test application...")
try:
    class TestApp(App):
        def build(self):
            layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
            layout.add_widget(Label(text='Label Printer GUI Test', size_hint_y=0.2))
            layout.add_widget(Label(text='✓ All components loaded successfully!', size_hint_y=0.3))
            btn = Button(text='Close', size_hint_y=0.2)
            btn.bind(on_press=lambda x: App.get_running_app().stop())
            layout.add_widget(btn)
            return layout
    
    print("✓ Test application created")
    print()
    print("=" * 60)
    print("🚀 Starting test GUI (close window to continue)...")
    print("=" * 60)
    
    app = TestApp()
    app.run()
    
    print()
    print("✓ GUI test completed successfully!")
    
except Exception as e:
    print(f"✗ Test application failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
