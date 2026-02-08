# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['idec_plc_password_auto.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['pywinauto', 'pywinauto.application', 'pywinauto.controls', 'pywinauto.findwindows', 'pywinauto.timings', 'comtypes', 'comtypes.client'],
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
    name='IDEC_PLC_Password_Finder',
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
    version='version_info.txt',
)
