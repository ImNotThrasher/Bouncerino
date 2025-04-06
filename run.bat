@echo off
setlocal
color 0A

echo Verificando e instalando dependencias...

pip install -r requirements.txt >temp_log.txt 2>&1
if %errorlevel% neq 0 (
    color 0C
    echo ❌ Error al instalar las dependencias.
    echo Detalles:
    type temp_log.txt
    del temp_log.txt
    pause
    exit /b
) else (
    echo ✅ Dependencias instaladas correctamente.
    del temp_log.txt
)

echo.
echo Ejecutando bouncerino desde src...
echo ------------------------------
python src\\bouncerino.py
echo ------------------------------
pause
endlocal
