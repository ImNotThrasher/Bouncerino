@echo off
echo Compilando Bouncerino...
pyinstaller --onefile --windowed --add-data "src\\image.png;." --add-data "src\\config.ini;." src\\bouncerino.py

echo Renombrando a .scr
rename dist\\bouncerino.exe bouncerino.scr

echo Build completo. Revisa la carpeta dist\\
pause
