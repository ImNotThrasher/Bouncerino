@echo off
chcp 65001 >nul
setlocal

:: ---------------------------
:: Instalador Bouncerino.scr
:: ---------------------------

set "NAME=Bouncerino"
set "DEFAULT_DIR=%WINDIR%\System32"
set "SRC_SCR=dist\%NAME%.scr"
set "APPDATA_DIR=%APPDATA%\%NAME%"

:: 1) Preguntar carpeta (ENTER → DEFAULT_DIR)
:: echo.
:: set /P INSTALL_DIR="Ruta de instalacion para %NAME% (ENTER -> %DEFAULT_DIR%): "
if "%INSTALL_DIR%"=="" set "INSTALL_DIR=%DEFAULT_DIR%"

echo.
echo Instalando %NAME% ...
echo.

:: Mostrar rutas destino
:: echo .scr  → %INSTALL_DIR%\%NAME%.scr
:: echo config.ini → %APPDATA_DIR%\config.ini
:: echo image.png  → %APPDATA_DIR%\image.png
:: echo.

:: 2) Crear carpeta AppData
if not exist "%APPDATA_DIR%" (
    mkdir "%APPDATA_DIR%"
    echo Carpeta creada: %APPDATA_DIR%
) else (
    echo Carpeta existente: %APPDATA_DIR%
)
echo.

:: 3) Instalar el .scr
if not exist "%SRC_SCR%" (
    echo ERROR: no se encontro %SRC_SCR%
    pause
    exit /b 1
)
if exist "%INSTALL_DIR%\%NAME%.scr" (
    echo ⚠️ .scr ya existe en: %INSTALL_DIR%\%NAME%.scr
) else (
    copy "%SRC_SCR%" "%INSTALL_DIR%\%NAME%.scr" >nul
    echo ✅ .scr copiado a: %INSTALL_DIR%\%NAME%.scr
)
echo.

:: 4) Copiar config.ini
if exist "src\config.ini" (
    if exist "%APPDATA_DIR%\config.ini" (
        echo ⚠️ config.ini ya existe en: %APPDATA_DIR%\config.ini
    ) else (
        copy "src\config.ini" "%APPDATA_DIR%\config.ini" >nul
        echo ✅ config.ini copiado a: %APPDATA_DIR%\config.ini
    )
) else (
    echo ⚠️ src\config.ini no encontrado, omitiendo.
)
echo.

:: 5) Copiar image.png
if exist "src\image.png" (
    if exist "%APPDATA_DIR%\image.png" (
        echo ⚠️ image.png ya existe en: %APPDATA_DIR%\image.png
    ) else (
        copy "src\image.png" "%APPDATA_DIR%\image.png" >nul
        echo ✅ image.png copiado a: %APPDATA_DIR%\image.png
    )
) else (
    echo ⚠️ src\image.png no encontrado, omitiendo.
)
echo.

echo 🎉 Instalacion finalizada.
echo.

pause
endlocal
