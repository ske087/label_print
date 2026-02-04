# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['label_printer_gui.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['kivy', 'kivy.core.window', 'kivy.core.text', 'kivy.core.image', 'kivy.uix.boxlayout', 'kivy.uix.gridlayout', 'kivy.uix.label', 'kivy.uix.textinput', 'kivy.uix.button', 'kivy.uix.spinner', 'kivy.uix.scrollview', 'kivy.uix.popup', 'kivy.clock', 'kivy.graphics', 'PIL', 'barcode', 'reportlab', 'print_label', 'print_label_pdf'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='LabelPrinter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
