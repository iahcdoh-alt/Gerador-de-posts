@echo off
echo ================================================
echo INSTALACAO COMPLETA - VERSAO MODERNA
echo Gerador de Posts Instagram
echo ================================================
echo.

cd /d C:\Dev\Gerador-de-posts

echo [1/7] Removendo ambiente virtual antigo...
if exist venv (
    rmdir /s /q venv
)

echo.
echo [2/7] Criando novo ambiente virtual...
python -m venv venv

echo.
echo [3/7] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [4/7] Instalando dependencias (isso pode levar alguns minutos)...
pip install --no-cache-dir openai==1.12.0
pip install --no-cache-dir python-dotenv==1.0.0
pip install --no-cache-dir Pillow==10.2.0
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir customtkinter==5.2.2

echo.
echo [5/7] Verificando instalacoes...
pip list | findstr "openai python-dotenv Pillow requests customtkinter"

echo.
echo [6/7] Criando pasta de imagens...
if not exist generated_images mkdir generated_images

echo.
echo [7/7] Testando aplicacao...
echo.
echo ================================================
echo INICIANDO APLICACAO MODERNA...
echo ================================================
echo.

python main_gui_modern.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ================================================
    echo ERRO AO EXECUTAR!
    echo ================================================
    echo.
    echo Verifique o arquivo .env com sua chave da API
    echo.
    pause
    exit /b 1
)

echo.
echo ================================================
echo SUCESSO!
echo ================================================
pause
