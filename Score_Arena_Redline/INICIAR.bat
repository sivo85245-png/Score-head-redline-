@echo off
setlocal
cd /d "%~dp0"
if not exist "web\index.html" goto incompleto
py -3 -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul
if not errorlevel 1 goto launcher
rem Ignora o atalho da Microsoft Store quando Python nao esta instalado.
for /f "delims=" %%P in ('where python.exe 2^>nul ^| findstr /v /i "WindowsApps"') do (
    "%%P" -c "import sys; sys.exit(0 if sys.version_info >= (3,10) else 1)" >nul 2>nul
    if not errorlevel 1 (
        "%%P" servidor.py
        goto terminou
    )
)
echo Python nao encontrado. Abrindo o jogo sem instalacao...
echo Corrida, duelo e liga funcionam. Somente as medicoes Python ficam indisponiveis.
start "" "%~dp0web\index.html"
exit /b 0
:launcher
py -3 servidor.py
goto terminou
:terminou
if errorlevel 1 (
    echo.
    echo Nao foi possivel iniciar o servidor. O erro esta acima.
    echo Voce pode abrir ABRIR_JOGO.html para jogar sem Python.
    pause
)
exit /b
:incompleto
echo Extraia o ZIP inteiro antes de abrir. A pasta web nao foi encontrada.
pause
exit /b 1
