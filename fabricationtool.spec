# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['fabricationtool.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\fab\\assets\\styles.qss', 'assets\\\\'), ('C:\\fab\\assets\\icons\\', 'assets\\icons\\\\'), ('.\\assets\\fonts\\Roboto-Medium.ttf', 'assets\\fonts\\\\')],
    hiddenimports=['matplotlib.backends.backend_pdf', 'cryptography'],
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
    [],
    exclude_binaries=True,
    name='fabricationtool',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='fabricationtool',
)
