@echo off
:: ========================================
:: GERADOR PROFISSIONAL DE POSTS INSTAGRAM
:: Integrius Automações - 2025
:: ========================================

title Gerador de Posts para Instagram - Integrius Automações

echo.
echo ========================================
echo   GERADOR DE POSTS PARA INSTAGRAM
echo   Integrius Automações - 2025
echo ========================================
echo.

:: Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERRO] Python não encontrado!
    echo.
    echo Por favor, instale Python 3.8+ em:
    echo https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo [OK] Python encontrado!
echo.

:: Verificar se arquivo .env existe
if not exist ".env" (
    echo [AVISO] Arquivo .env não encontrado!
    echo.
    echo Criando .env a partir do .env.example...
    copy .env.example .env >nul
    echo.
    echo [ACAO NECESSARIA] Configure suas chaves de API no arquivo .env
    echo.
    echo 1. Abra o arquivo .env em um editor de texto
    echo 2. Adicione sua OPENAI_API_KEY
    echo 3. Adicione sua REPLICATE_API_TOKEN
    echo 4. Salve o arquivo e execute este script novamente
    echo.
    pause
    exit /b 1
)

echo [OK] Arquivo .env encontrado!
echo.

:: Verificar se dependências estão instaladas
echo Verificando dependências...
pip show ttkbootstrap >nul 2>&1
if errorlevel 1 (
    echo.
    echo [INSTALANDO] Instalando dependências...
    echo.
    pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [ERRO] Falha ao instalar dependências!
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [OK] Dependências instaladas com sucesso!
    echo.
) else (
    echo [OK] Dependências já instaladas!
    echo.
)

:: Executar o aplicativo
echo ========================================
echo   INICIANDO APLICATIVO...
echo ========================================
echo.

python instagram_post_generator.py

:: Se houver erro ao executar
if errorlevel 1 (
    echo.
    echo ========================================
    echo   ERRO AO EXECUTAR O APLICATIVO
    echo ========================================
    echo.
    echo Possíveis causas:
    echo - Chaves de API não configuradas corretamente no .env
    echo - Problema com dependências Python
    echo - Erro de conexão com internet
    echo.
    echo Verifique o arquivo .env e tente novamente.
    echo.
    pause
    exit /b 1
)

echo.
echo Aplicativo encerrado.
pause
