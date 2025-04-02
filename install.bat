@echo off
setlocal

echo Instalando Bouncerino...

set "WINSYS=%WINDIR%\\System32"
set "APPDATA_DIR=%APPDATA%\\Bouncerino"

:: Crear carpeta de recursos
if not exist "%APPDATA_DIR%" (
    mkdir "%APPDATA_DIR%"
)

:: Copiar archivos
copy /Y "dist\\bouncerino.scr" "%WINSYS%\\bouncerino.scr"
copy /Y "src\\config.ini" "%APPDATA_DIR%\\config.ini"
copy /Y "src\\image.png" "%APPDATA_DIR%\\image.png"

echo Instalación completada.
pause
endlocal
