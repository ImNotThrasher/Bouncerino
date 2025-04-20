@echo off
setlocal EnableDelayedExpansion

:: --------------------------------------------------
:: Configuración de variables (fáciles de ajustar)
:: --------------------------------------------------
set "APP_NAME=Bouncerino"
set "SRC_FILE=src\bouncerino.py"
set "ICON_FILE=src\image.png"
set "CONFIG_FILE=src\config.ini"
set "DIST_DIR=dist"
set "BUILD_DIR=build"
set "SPEC_FILE=%APP_NAME%.spec"
set "OUTPUT_EXE=%DIST_DIR%\%APP_NAME%.exe"
set "OUTPUT_SCR=%DIST_DIR%\%APP_NAME%.scr"

:: --------------------------------------------------
:: Limpieza de builds anteriores
:: --------------------------------------------------
echo Limpiando builds anteriores...
if exist "%OUTPUT_SCR%" (
    echo  - Eliminando antiguo %APP_NAME%.scr
    del /f /q "%OUTPUT_SCR%"
)
if exist "%OUTPUT_EXE%" (
    echo  - Eliminando antiguo %APP_NAME%.exe
    del /f /q "%OUTPUT_EXE%"
)
if exist "%BUILD_DIR%" (
    echo  - Eliminando carpeta %BUILD_DIR%
    rmdir /s /q "%BUILD_DIR%"
)
if exist "%SPEC_FILE%" (
    echo  - Eliminando archivo %SPEC_FILE%
    del /f /q "%SPEC_FILE%"
)
echo.

:: --------------------------------------------------
:: Compilación con PyInstaller
:: --------------------------------------------------
echo Compilando %APP_NAME%...
echo.
pyinstaller --onefile --windowed ^
    --add-data "%ICON_FILE%;." ^
    --add-data "%CONFIG_FILE%;." ^
    --name "%APP_NAME%" ^
    "%SRC_FILE%"
if errorlevel 1 (
    echo ERROR: Falló la compilación con PyInstaller.
    pause
    exit /b 1
)

:: --------------------------------------------------
:: Renombrar .exe a .scr (sobre-escribiendo si ya existe)
:: --------------------------------------------------
echo Renombrando a .scr...
if exist "%OUTPUT_SCR%" (
    echo  - %OUTPUT_SCR% ya existe, será sobreescrito.
    del /f /q "%OUTPUT_SCR%"
)
rename "%OUTPUT_EXE%" "%APP_NAME%.scr"

:: --------------------------------------------------
:: Mensaje final
:: --------------------------------------------------
echo.
echo Build completado con éxito.
echo Revisa la carpeta %DIST_DIR%\ para encontrar %APP_NAME%.scr
echo.
pause
endlocal
