@echo off
setlocal EnableDelayedExpansion

:: Nombre del screensaver (base para archivos)
set "NAME=Bouncerino"

:: Detectar modo silent
set SILENT=0
if /I "%1"=="-silent" set SILENT=1
if /I "%1"=="/silent" set SILENT=1

if !SILENT! EQU 0 (
    color 0A
    echo Instalando !NAME!...
)

set "WINSYS=%WINDIR%\System32"
set "APPDATA_DIR=%APPDATA%\!NAME!"
set "SRC_FILE=dist\!NAME!.scr"
set "DEST_FILE=%WINSYS%\!NAME!.scr"
set "LOG_FILE=%APPDATA_DIR%\install_log.txt"

if not exist "!APPDATA_DIR!" (
    mkdir "!APPDATA_DIR!"
)

if exist "!SRC_FILE!" (
    copy /Y "!SRC_FILE!" "!DEST_FILE!" >nul
    if !SILENT! EQU 0 echo ✅ Screensaver instalado en: !DEST_FILE!

    if exist "src\config.ini" (
        copy /Y "src\config.ini" "!APPDATA_DIR!\config.ini"
    ) else (
        if !SILENT! EQU 0 echo ⚠️ No se encontró src\config.ini
        echo [%DATE% %TIME%] config.ini no encontrado >> "!LOG_FILE!"
    )

    if exist "src\image.png" (
        copy /Y "src\image.png" "!APPDATA_DIR!\image.png"
    ) else (
        if !SILENT! EQU 0 echo ⚠️ No se encontró src\image.png
        echo [%DATE% %TIME%] image.png no encontrado >> "!LOG_FILE!"
    )

    if !SILENT! EQU 0 echo Instalación completada.
) else (
    color 0C
    echo ❌ No se pudo instalar: no se encontró !SRC_FILE!
    echo [%DATE% %TIME%] ERROR: !NAME!.scr no encontrado >> "!LOG_FILE!"
)

if !SILENT! EQU 0 pause
endlocal
