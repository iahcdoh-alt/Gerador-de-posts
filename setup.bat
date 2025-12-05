@echo off
echo ==========================================
echo   INSTALACAO - GERADOR DE POSTS INSTAGRAM
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

REM Criar ambiente virtual
echo Criando ambiente virtual...
python -m venv venv

if errorlevel 1 (
    echo X Erro ao criar ambiente virtual
    pause
    exit /b 1
)

echo OK Ambiente virtual criado com sucesso!
echo.

REM Ativar ambiente virtual
echo Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Atualizar pip
echo Atualizando pip...
python -m pip install --upgrade pip >nul 2>&1

REM Instalar dependências
echo Instalando dependencias...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Erro ao instalar dependencias
    pause
    exit /b 1
)

echo OK Dependencias instaladas com sucesso!
echo.

REM Criar arquivo .env se não existir
if not exist .env (
    echo Criando arquivo de configuracao...
    copy .env.example .env
    echo OK Arquivo .env criado!
    echo.
    echo IMPORTANTE: Edite o arquivo .env e adicione sua chave da API OpenAI
    echo.
) else (
    echo Arquivo .env ja existe
    echo.
)

REM Criar diretório para imagens geradas
if not exist generated_images (
    mkdir generated_images
    echo OK Diretorio 'generated_images' criado!
)

echo.
echo ==========================================
echo   OK INSTALACAO CONCLUIDA COM SUCESSO!
echo ==========================================
echo.
echo PROXIMOS PASSOS:
echo.
echo 1. Edite o arquivo .env e adicione sua API Key da OpenAI
echo.
echo 2. Ative o ambiente virtual:
echo    venv\Scripts\activate.bat
echo.
echo 3. Execute a aplicacao:
echo    python main.py
echo.
echo ==========================================
pause
