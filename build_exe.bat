@echo off
:: ========================================
:: BUILD EXECUTAVEL - Instagram Generator
:: Integrius Automações - 2025
:: ========================================

echo.
echo ========================================
echo  CRIANDO EXECUTAVEL WINDOWS (.EXE)
echo ========================================
echo.

:: Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python nao encontrado!
    pause
    exit /b 1
)

echo [1/4] Instalando PyInstaller...
pip install pyinstaller

echo.
echo [2/4] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [3/4] Criando executavel (pode demorar alguns minutos)...
pyinstaller --noconfirm --onefile --windowed ^
    --name "Instagram_Post_Generator" ^
    --icon=NONE ^
    --add-data ".env.example;." ^
    --add-data "README_INSTAGRAM_GENERATOR.md;." ^
    --add-data "GUIA_RAPIDO.md;." ^
    --hidden-import=ttkbootstrap ^
    --hidden-import=replicate ^
    --hidden-import=openai ^
    --hidden-import=PIL ^
    --hidden-import=dotenv ^
    instagram_post_generator.py

echo.
echo [4/4] Copiando arquivo .env.example para dist...
copy .env.example dist\.env.example

echo.
echo ========================================
echo  EXECUTAVEL CRIADO COM SUCESSO!
echo ========================================
echo.
echo Localizacao: dist\Instagram_Post_Generator.exe
echo.
echo IMPORTANTE:
echo 1. Copie o arquivo .env.example para a pasta dist\
echo 2. Renomeie para .env
echo 3. Configure suas chaves de API
echo 4. Execute Instagram_Post_Generator.exe
echo.
pause
