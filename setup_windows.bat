@echo off
echo ========================================
echo Setup do Gerador de Posts no Windows
echo ========================================
echo.

REM Definir caminhos
set "DEST_DIR=C:\Dev\Gerador-de-posts"
set "WSL_PATH=\\wsl$\Ubuntu\home\hans\Gerador-de-posts"

echo [1/6] Verificando se Python esta instalado...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO: Python nao encontrado!
    echo.
    echo Por favor, instale Python primeiro:
    echo https://www.python.org/downloads/
    echo.
    echo Durante a instalacao, marque "Add Python to PATH"
    echo.
    pause
    exit /b 1
)
echo Python encontrado!

echo.
echo [2/6] Criando pasta de destino...
if not exist "C:\Dev" mkdir "C:\Dev"
if exist "%DEST_DIR%" (
    echo Pasta ja existe. Deseja sobrescrever? (S/N)
    choice /C SN /N
    if errorlevel 2 (
        echo Operacao cancelada.
        pause
        exit /b 0
    )
    echo Removendo pasta antiga...
    rmdir /s /q "%DEST_DIR%"
)
mkdir "%DEST_DIR%"

echo.
echo [3/6] Copiando arquivos do WSL2 para Windows...
echo Isso pode levar alguns minutos...
robocopy "%WSL_PATH%" "%DEST_DIR%" /E /XD venv __pycache__ .git generated_images dist build installer_output Output /XF *.pyc *.pyo *.log /NJH /NJS /NDL /NC /NS

if %ERRORLEVEL% GEQ 8 (
    echo.
    echo ERRO ao copiar arquivos!
    echo Verifique se o caminho WSL2 esta correto.
    pause
    exit /b 1
)

echo.
echo [4/6] Criando ambiente virtual...
cd /d "%DEST_DIR%"
python -m venv venv

echo.
echo [5/6] Instalando dependencias...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO ao instalar dependencias!
    pause
    exit /b 1
)

echo.
echo [6/6] Copiando arquivo .env...
if exist "%WSL_PATH%\.env" (
    copy "%WSL_PATH%\.env" "%DEST_DIR%\.env" >nul
    echo Arquivo .env copiado!
) else (
    if not exist "%DEST_DIR%\.env" (
        echo AVISO: Arquivo .env nao encontrado.
        echo Criando .env a partir do .env.example...
        if exist "%DEST_DIR%\.env.example" (
            copy "%DEST_DIR%\.env.example" "%DEST_DIR%\.env" >nul
            echo.
            echo *** IMPORTANTE ***
            echo Edite o arquivo .env e adicione sua chave da API OpenAI!
            echo Caminho: %DEST_DIR%\.env
        )
    )
)

echo.
echo ========================================
echo SETUP CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Projeto copiado para: %DEST_DIR%
echo.
echo Para executar a versao MODERNA:
echo 1. cd %DEST_DIR%
echo 2. venv\Scripts\activate
echo 3. python main_gui_modern.py
echo.
echo Para executar a versao CLASSICA:
echo 1. cd %DEST_DIR%
echo 2. venv\Scripts\activate
echo 3. python main_gui.py
echo.
echo ========================================
echo.
echo Deseja executar a versao moderna AGORA? (S/N)
choice /C SN /N
if errorlevel 2 goto :fim

echo.
echo Iniciando aplicacao moderna...
python main_gui_modern.py

:fim
echo.
pause
