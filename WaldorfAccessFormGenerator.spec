# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[('assets', 'assets'), ('source', 'source'), ('waldodb-74088-firebase-adminsdk-fbsvc-37790af852.json', '.'), ('.env', '.')],
    hiddenimports=['sip', 'fpdf', 'fpdf.pdf', 'fpdf.template', 'PIL', 'PIL.Image', 'PyQt5', 'PyQt5.QtCore', 'PyQt5.QtGui', 'PyQt5.QtWidgets', 'firebase_admin', 'firebase_admin.credentials', 'firebase_admin.db', 'google.cloud', 'google.oauth2', 'google.auth', 'dotenv', 'config', 'source.database.db_manager', 'source.GUI', 'source.GUI.login_screen', 'source.GUI.main_screen', 'source.GUI.Form', 'source.GUI.departments_and_positions', 'source.GUI.hotel_systems', 'source.GUI.navigation_bar', 'source.Templates', 'source.Templates.access_template_generator', 'source.Templates.departure_template'],
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
    name='WaldorfAccessFormGenerator',
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
    icon=['assets\\waldorf_ico.ico'],
)
