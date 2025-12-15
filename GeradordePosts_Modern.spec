# -*- mode: python ; coding: utf-8 -*-

import os
import sys
from PyInstaller.utils.hooks import collect_data_files, collect_submodules

# Coletar dados do customtkinter
customtkinter_datas = collect_data_files('customtkinter')

block_cipher = None

a = Analysis(
    ['main_gui_modern.py'],
    pathex=[],
    binaries=[],
    datas=customtkinter_datas,
    hiddenimports=[
        'openai',
        'dotenv',
        'PIL',
        'PIL._tkinter_finder',
        'requests',
        'customtkinter',
    ] + collect_submodules('customtkinter'),
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
    [],
    exclude_binaries=True,
    name='GeradordePosts_Modern',
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
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='GeradordePosts_Modern',
)

# Copiar arquivos necessários
import shutil
import os

dist_path = os.path.join(DISTPATH, 'GeradordePosts_Modern')

# Criar pasta para imagens
images_dir = os.path.join(dist_path, 'generated_images')
os.makedirs(images_dir, exist_ok=True)

# Copiar .env.example se existir
env_example = '.env.example'
if os.path.exists(env_example):
    shutil.copy(env_example, os.path.join(dist_path, env_example))

print("\n" + "="*70)
print("BUILD CONCLUÍDO COM SUCESSO!")
print("="*70)
print(f"\nExecutável criado em: {dist_path}")
print("\nPróximos passos:")
print("1. Copie o arquivo .env com sua chave da API para a pasta dist")
print("2. Execute: dist/GeradordePosts_Modern/GeradordePosts_Modern.exe")
print("="*70 + "\n")
