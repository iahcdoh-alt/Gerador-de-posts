# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['instagram_post_generator.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README_INSTAGRAM_GENERATOR.md', '.'),
        ('GUIA_RAPIDO.md', '.'),
    ],
    hiddenimports=[
        'ttkbootstrap',
        'ttkbootstrap.themes',
        'ttkbootstrap.constants',
        'ttkbootstrap.scrolled',
        'ttkbootstrap.toast',
        'replicate',
        'openai',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'dotenv',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='Instagram_Post_Generator',
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
