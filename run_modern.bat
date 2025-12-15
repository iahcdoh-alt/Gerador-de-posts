@echo off
echo ========================================
echo Executar Versao Moderna
echo Gerador de Posts Instagram
echo ========================================
echo.

REM Ativar ambiente virtual se existir
if exist "venv\Scripts\activate.bat" (
    echo Ativando ambiente virtual...
    call venv\Scripts\activate.bat
)

echo Executando aplicacao moderna...
echo.
python main_gui_modern.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERRO ao executar!
    echo.
    echo Certifique-se de ter instalado as dependencias:
    echo pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)
