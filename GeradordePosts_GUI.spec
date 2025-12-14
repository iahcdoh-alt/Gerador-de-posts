# -*- mode: python ; coding: utf-8 -*-
# Arquivo de configuração do PyInstaller para Gerador de Posts Instagram - Versão GUI

block_cipher = None

a = Analysis(
    ['main_gui.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('.env.example', '.'),
    ],
    hiddenimports=[
        'openai',
        'dotenv',
        'PIL',
        'PIL._tkinter_finder',
        'requests',
        'tkinter',
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
    name='GeradordePosts_GUI',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Não mostrar console (janela preta)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Você pode adicionar um ícone .ico aqui
)
