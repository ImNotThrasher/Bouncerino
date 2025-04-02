@echo off
setlocal

echo Desinstalando Bouncerino...

set "WINSYS=%WINDIR%\\System32"
set "APPDATA_DIR=%APPDATA%\\Bouncerino"

:: Borrar .scr
del /Q "%WINSYS%\\bouncerino.scr"

:: Borrar config e imagen
rd /S /Q "%APPDATA_DIR%"

echo Desinstalación completada.
pause
endlocal
