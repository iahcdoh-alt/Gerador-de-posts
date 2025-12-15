@echo off
echo ================================================
echo INSTALACAO VERSAO MODERNA FINAL
echo Gerador de Posts Instagram - Integrius Automacoes
echo ================================================
echo.

cd /d C:\Dev\Gerador-de-posts

echo [1/8] Fazendo backup da versao antiga...
if exist main_gui.py (
    copy main_gui.py main_gui_backup.py >nul
    echo Backup criado: main_gui_backup.py
)

echo.
echo [2/8] Baixando atualizacoes do repositorio...
git pull origin claude/instagram-post-generator-015rv43969TpLRSirW4HPmD6

echo.
echo [3/8] Removendo ambiente virtual antigo...
if exist venv (
    rmdir /s /q venv
)

echo.
echo [4/8] Criando novo ambiente virtual...
python -m venv venv

echo.
echo [5/8] Ativando ambiente virtual...
call venv\Scripts\activate.bat

echo.
echo [6/8] Instalando dependencias (isso pode levar alguns minutos)...
pip install --no-cache-dir openai==1.12.0
pip install --no-cache-dir python-dotenv==1.0.0
pip install --no-cache-dir Pillow==10.2.0
pip install --no-cache-dir requests==2.31.0
pip install --no-cache-dir ttkbootstrap==1.10.1

echo.
echo [7/8] Substituindo arquivo principal...
copy main_gui_new.py main_gui.py /Y >nul
echo Arquivo main_gui.py atualizado com versao moderna!

echo.
echo [8/8] Criando pasta de imagens...
if not exist generated_images mkdir generated_images

echo.
echo ================================================
echo INSTALACAO CONCLUIDA COM SUCESSO!
echo ================================================
echo.
echo Versao moderna com TTKBootstrap instalada!
echo - Tema Dark/Light
echo - Visual moderno
echo - Rodape Integrius Automacoes
echo.
echo ================================================
echo TESTANDO APLICACAO...
echo ================================================
echo.

python main_gui.py

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
echo.
echo Para compilar o executavel:
echo pyinstaller --clean GeradordePosts_GUI.spec
echo.
pause
