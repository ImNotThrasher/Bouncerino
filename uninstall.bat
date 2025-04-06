@echo off
setlocal EnableDelayedExpansion

:: Detectar modo silent
set SILENT=0
if /I "%1"=="-silent" set SILENT=1
if /I "%1"=="/silent" set SILENT=1

if !SILENT! EQU 0 (
    color 0A
    echo Desinstalando Bouncerino...
)

set "WINSYS=%WINDIR%\System32"
set "APPDATA_DIR=%APPDATA%\Bouncerino"
set "DEST_FILE=%WINSYS%\bouncerino.scr"
set "LOG_FILE=%APPDATA_DIR%\uninstall_log.txt"

if exist "%DEST_FILE%" (
    del /Q "%DEST_FILE%"
    if !SILENT! EQU 0 echo ✅ Screensaver eliminado: %DEST_FILE%
) else (
    color 0E
    if !SILENT! EQU 0 echo ⚠️ No se encontró screensaver en: %DEST_FILE%
    echo [%DATE% %TIME%] Advertencia: bouncerino.scr no encontrado durante desinstalación >> "%LOG_FILE%"
)

rd /S /Q "%APPDATA_DIR%"
if !SILENT! EQU 0 echo (Carpeta de recursos eliminada: %APPDATA_DIR%)

if !SILENT! EQU 0 echo Desinstalación completada.
if !SILENT! EQU 0 pause
endlocal
