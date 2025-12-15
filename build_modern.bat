@echo off
echo ========================================
echo Compilador da Versao Moderna
echo Gerador de Posts Instagram
echo ========================================
echo.

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo [1/4] Ativando ambiente virtual...
    call venv\Scripts\activate.bat
) else (
    echo AVISO: Ambiente virtual nao encontrado
    echo Usando Python do sistema...
    echo.
)

echo [2/4] Verificando dependencias...
pip show customtkinter >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo CustomTkinter nao encontrado! Instalando...
    pip install customtkinter
)

echo [3/4] Limpando builds anteriores...
if exist "dist\GeradordePosts_Modern" (
    rmdir /s /q "dist\GeradordePosts_Modern"
)
if exist "build" (
    rmdir /s /q "build"
)

echo [4/4] Compilando aplicacao moderna...
pyinstaller --clean GeradordePosts_Modern.spec

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO ao compilar!
    pause
    exit /b 1
)

echo.
echo ========================================
echo BUILD CONCLUIDO COM SUCESSO!
echo ========================================
echo.
echo Executavel criado em:
echo dist\GeradordePosts_Modern\GeradordePosts_Modern.exe
echo.
echo Proximos passos:
echo 1. Copie o arquivo .env para: dist\GeradordePosts_Modern\
echo 2. Execute: dist\GeradordePosts_Modern\GeradordePosts_Modern.exe
echo.
pause
