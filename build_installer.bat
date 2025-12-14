@echo off
echo ========================================
echo Compilador de Instalador
echo Gerador de Posts Instagram
echo ========================================
echo.

REM Verificar se Inno Setup está instalado
set INNO_COMPILER="C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist %INNO_COMPILER% (
    echo ERRO: Inno Setup nao encontrado!
    echo.
    echo Por favor, instale o Inno Setup primeiro:
    echo https://jrsoftware.org/isdl.php
    echo.
    echo Baixe a versao: innosetup-6.x.x.exe
    pause
    exit /b 1
)

echo [1/3] Verificando executavel...
if not exist "dist\GeradordePosts_GUI.exe" (
    echo ERRO: Executavel nao encontrado!
    echo Execute primeiro: pyinstaller --clean GeradordePosts_GUI.spec
    pause
    exit /b 1
)

echo [2/3] Compilando instalador...
%INNO_COMPILER% installer_setup.iss

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO ao compilar instalador!
    pause
    exit /b 1
)

echo [3/3] Instalador criado com sucesso!
echo.
echo ========================================
echo Instalador criado em:
echo installer_output\GeradordePosts_Installer.exe
echo ========================================
echo.
echo Voce pode distribuir este arquivo!
echo.
pause
