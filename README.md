# 🎛️ bouncerino

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![pygame](https://img.shields.io/badge/pygame-2.x-green)
![License](https://img.shields.io/badge/license-MIT-lightgrey)
![Status](https://img.shields.io/badge/version-0.9.0-yellow)

**bouncerino** es un protector de pantalla escrito en Python con Pygame. Muestra un logo rebotando por la pantalla y genera pequeñas copias con rotación opcional cada vez que rebota. Es configurable, portátil y se puede ejecutar como `.py`, `.exe` o `.scr` en Windows.

---

## 📁 Estructura del proyecto

```
bouncerino/
├── src/
│   ├── bouncerino.py         # Código principal del screensaver
│   ├── config.ini            # Configuración editable (opcional)
│   └── image.png             # Imagen que rebota por la pantalla
├── dist/                     # Carpeta generada por PyInstaller (.exe o .scr)
├── build.bat                 # Script para compilar el .scr desde el .py
├── run.bat                   # Script para ejecutar el screensaver directamente
├── install.bat               # Instalador: copia archivos al sistema
├── uninstall.bat             # Desinstalador: borra archivos del sistema
├── requirements.txt          # Dependencias de Python
├── LICENSE                   # Licencia del proyecto (MIT)
└── README.md                 # Documentación del proyecto
```

---

## 🧰 Requisitos

Este proyecto incluye un archivo [`requirements.txt`](./requirements.txt) que facilita la instalación de dependencias:

```bash
pip install -r requirements.txt
```

Requiere:
- Python 3.8 o superior
- pygame
- (opcional) pyinstaller para generar ejecutables

---

## ⚙️ Configuración (`config.ini`)

📌 El archivo [`config.ini`](src/config.ini) es **opcional**. Si no se encuentra, se usan valores por defecto.

### 📍 Ubicaciones soportadas:
- `%APPDATA%\bouncerino\config.ini`
- Misma carpeta donde se encuentra el `.scr`, `.exe` o `.py`

### 🔄 Prioridad de búsqueda de archivos

Al ejecutarse, **bouncerino primero busca archivos en esta prioridad**:

1. `%APPDATA%\bouncerino\` → si está instalado con `install.bat`.
2. Carpeta local → donde esté el `.exe`, `.scr` o `.py`.

Esto aplica tanto a [`config.ini`](src/config.ini), [`image.png`](src/image.png) como `ARCHIVO_FONDO`.

### Ejemplo completo (`config.ini`):

```ini
[CONFIG]

; -------------------
; Pantalla y fondo
; -------------------
NOMBRE_SCREENSAVER = Bouncerino
COLOR_FONDO = 0, 0, 0
ARCHIVO_FONDO =

; -------------------
; Imagen principal
; -------------------
ARCHIVO_IMAGEN = image.png
ANCHO_BASE = 400
VELOCIDAD_REBOTE = 3

; -------------------
; Clones pequeños
; -------------------
MAX_ELEMENTOS = 100
ROTACION_CLONES_ACTIVADA = True
VELOCIDAD_CLONES_ROTACION = 3

; -------------------
; Rendimiento
; -------------------
TIEMPO_ESPERA = 10
```

---

## ▶️ Ejecución

### 🪟 Modo ventana (desarrollo)

Podés ejecutar [`bouncerino.py`](src/bouncerino.py) con el argumento `--ventana` para que corra en modo **ventana**, en lugar de pantalla completa:

```bash
python src/bouncerino.py --ventana
```

### 🐍 Ejecutar normalmente

```bash
python src/bouncerino.py
```

### 🖱️ O usar el script `run.bat`

```bash
run.bat
```

---

## 🔨 Compilar como `.scr` (screensaver)

Usá el script `build.bat` para generar `bouncerino.scr` con PyInstaller:

Esto:
- Crea un `.exe` desde `src/bouncerino.py` usando PyInstaller
- Lo renombra a `.scr`
- Lo guarda en `dist/bouncerino.scr`


```bash
build.bat
```

---

## 📥 Instalación como screensaver de Windows

Ejecutá:

```bash
install.bat
```

Esto:
- Copia `bouncerino.scr` a `%WINDIR%\System32` (ubicación obligatoria para protectores de pantalla en Windows)
- Copia `config.ini` e `image.png` a `%APPDATA%\bouncerino` (carpeta de recursos y configuración)

### 🤫 Modo silencioso

Los scripts `install.bat` y `uninstall.bat` aceptan `-silent` o `/silent` para ocultar mensajes:

```bash
install.bat -silent
```

---

## ❌ Desinstalación

```bash
uninstall.bat
```

Elimina el `.scr` de System32 y los recursos de `%APPDATA%\bouncerino`.

---

## 🧠 Comportamiento del programa

- Se cierra si:
  - Tocás una tecla
  - Clickeás el mouse
  - Movés el mouse

- Si no se encuentran los archivos de imagen/config:
  - Usa valores por defecto
  - Muestra una imagen roja de reemplazo

---

## 📄 Licencia

Este proyecto está bajo la licencia MIT.  
Ver el archivo [`LICENSE`](./LICENSE) para más información.
