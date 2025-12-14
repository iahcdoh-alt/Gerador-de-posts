@echo off
echo ==========================================
echo   BUILD GUI - GERADOR DE POSTS INSTAGRAM
echo ==========================================
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python nao encontrado!
    echo Por favor, instale Python 3.8 ou superior
    pause
    exit /b 1
)

echo OK Python encontrado
echo.

REM Ativar ambiente virtual se existir
if exist venv\Scripts\activate.bat (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo Criando ambiente virtual...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.

REM Instalar dependências de desenvolvimento
echo Instalando PyInstaller...
pip install -r requirements-dev.txt

if errorlevel 1 (
    echo X Erro ao instalar PyInstaller
    pause
    exit /b 1
)

echo.

REM Instalar dependências principais
echo Instalando dependencias principais...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Erro ao instalar dependencias
    pause
    exit /b 1
)

echo.

REM Limpar builds anteriores
if exist build (
    echo Limpando builds anteriores...
    rmdir /s /q build
)
if exist dist (
    rmdir /s /q dist
)

echo.

REM Gerar executável GUI
echo ==========================================
echo   GERANDO EXECUTAVEL GUI...
echo ==========================================
echo.
echo Isso pode levar alguns minutos...
echo.

pyinstaller GeradordePosts_GUI.spec

if errorlevel 1 (
    echo.
    echo X Erro ao gerar executavel
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   OK BUILD GUI CONCLUIDO COM SUCESSO!
echo ==========================================
echo.
echo O executavel GUI foi gerado em: dist\GeradordePosts_GUI.exe
echo.
echo IMPORTANTE:
echo 1. Copie o arquivo .env para a pasta dist\
echo 2. Copie a pasta generated_images para dist\ (se existir)
echo 3. Execute dist\GeradordePosts_GUI.exe
echo.
echo DIFERENCA ENTRE CLI E GUI:
echo - GeradordePosts.exe: Interface de terminal (CLI)
echo - GeradordePosts_GUI.exe: Interface grafica com janelas (GUI)
echo.
echo ==========================================

REM Criar estrutura na pasta dist
if not exist dist\.env (
    if exist .env (
        echo Copiando arquivo .env...
        copy .env dist\.env
    ) else (
        echo Copiando .env.example...
        copy .env.example dist\.env.example
    )
)

if not exist dist\generated_images (
    echo Criando pasta generated_images...
    mkdir dist\generated_images
)

echo.
echo OK Arquivos copiados!
echo.
echo Voce pode encontrar o executavel GUI em: dist\GeradordePosts_GUI.exe
echo.

pause
