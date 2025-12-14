@echo off
echo ==========================================
echo   BUILD COMPLETO - CLI + GUI
echo   GERADOR DE POSTS INSTAGRAM
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

REM Instalar dependências
echo Instalando dependencias...
pip install -r requirements-dev.txt
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
echo ==========================================
echo   GERANDO VERSAO CLI...
echo ==========================================
echo.

pyinstaller GeradordePosts.spec

if errorlevel 1 (
    echo X Erro ao gerar versao CLI
    pause
    exit /b 1
)

echo.
echo OK Versao CLI gerada com sucesso!
echo.

REM Limpar pasta build antes da segunda compilação
if exist build (
    rmdir /s /q build
)

echo.
echo ==========================================
echo   GERANDO VERSAO GUI...
echo ==========================================
echo.

pyinstaller GeradordePosts_GUI.spec

if errorlevel 1 (
    echo X Erro ao gerar versao GUI
    pause
    exit /b 1
)

echo.
echo ==========================================
echo   OK BUILD COMPLETO CONCLUIDO!
echo ==========================================
echo.
echo Ambos os executaveis foram gerados na pasta dist\:
echo.
echo 1. GeradordePosts.exe - Interface de terminal (CLI)
echo 2. GeradordePosts_GUI.exe - Interface grafica com janelas (GUI)
echo.

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
echo ==========================================
echo   COMO USAR:
echo ==========================================
echo.
echo 1. Edite dist\.env e adicione sua API Key
echo 2. Para interface de terminal: Execute dist\GeradordePosts.exe
echo 3. Para interface grafica: Execute dist\GeradordePosts_GUI.exe
echo.
echo Ambas as versoes tem as mesmas funcionalidades!
echo A diferenca e apenas na forma de interacao.
echo.

pause
