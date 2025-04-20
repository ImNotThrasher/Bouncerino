@echo off
chcp 65001 >nul
setlocal EnableDelayedExpansion

:: -------------------------
::  Desinstalador Bouncerino
:: -------------------------

:: Nombre base
set "NAME=Bouncerino"
set "DEFAULT_DIR=%WINDIR%\System32"
set "APPDATA_DIR=%APPDATA%\%NAME%"

:: 1) Preguntar ruta de instalación
:: echo.
:: set /P INSTALL_DIR="Ruta de instalación de %NAME% (ENTER -> %DEFAULT_DIR%): "
if "%INSTALL_DIR%"=="" set "INSTALL_DIR=%DEFAULT_DIR%"

echo.
echo Desinstalando %NAME% ...
echo.

:: 2) Intentar borrar el .scr
set "SCR=%INSTALL_DIR%\%NAME%.scr"
:: echo Buscando screensaver: %SCR%
if exist "%SCR%" (
    del /Q "%SCR%" 2>nul
    if exist "%SCR%" (
        echo ❌ No se pudo borrar: %SCR%
    ) else (
        echo ✅ Borrado correctamente: %SCR%
    )
) else (
    echo ⚠️  No encontrado: %SCR%
)
echo.

:: 3) Intentar borrar config.ini e image.png en AppData
if exist "%APPDATA_DIR%" (
    for %%F in (config.ini image.png) do (
        set "FILE=%APPDATA_DIR%\%%F"
        :: echo Buscando recurso: !FILE!
        if exist "!FILE!" (
            del /Q "!FILE!" 2>nul
            if exist "!FILE!" (
                echo ❌ No se pudo borrar: !FILE!
            ) else (
                echo ✅ Borrado correctamente: !FILE!
            )
        ) else (
            echo ⚠️  No encontrado: !FILE!
        )
        echo.
    )
) else (
    echo ⚠️  Carpeta de AppData no existe: %APPDATA_DIR%
    echo.
)

:: 4) Limpiar backups (^>7 días) si se pidió
if "%CLEAN_BAK%"=="1" if exist "%APPDATA_DIR%" (
    echo Limpiando backups ^>7 días en: %APPDATA_DIR%
    forfiles /P "%APPDATA_DIR%" /M "*.bak" /D -7 /C "cmd /c del /Q @path" 2>nul
    echo 🧹 Backups antiguos eliminados ^(si existían^).
    echo.
)

:: 5) Quitar clave de registro
echo Eliminando clave SCRNSAVE.EXE del registro...
reg delete "HKCU\Control Panel\Desktop" /V SCRNSAVE.EXE /F >nul 2>&1 && (
    echo ✅ Clave eliminada
) || (
    echo ⚠️  Clave no encontrada o no pudo eliminarse
)
echo.

:: 6) Intentar borrar carpeta de AppData completa
if exist "%APPDATA_DIR%" (
    echo Intentando borrar carpeta de AppData: %APPDATA_DIR%
    rd /S /Q "%APPDATA_DIR%" 2>nul
    if exist "%APPDATA_DIR%" (
        echo ❌ No se pudo borrar la carpeta: %APPDATA_DIR%
    ) else (
        echo ✅ Carpeta de AppData eliminada
    )
) else (
    echo ⚠️  Carpeta de AppData ya no existe: %APPDATA_DIR%
)
echo.

echo 🎉 Desinstalación completada.
echo.

pause
endlocal
