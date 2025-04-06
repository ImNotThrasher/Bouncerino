# 🎛️ bouncerino

**bouncerino** es un screensaver (protector de pantalla) hecho en Python con Pygame que simula un logo rebotando por la pantalla. Cada vez que el logo rebota, genera pequeñas versiones que también se mueven y pueden rotar si se activa esa opción.

Este proyecto permite configuración flexible mediante un archivo `config.ini`, y puede ser ejecutado como `.py`, `.exe` o `.scr` (screensaver de Windows).

---

## 📦 Estructura del proyecto

```plaintext
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
└── README.md                 # Documentación del proyecto
```
---

## 🧰 Requisitos

Este proyecto incluye un archivo `requirements.txt` que facilita la instalación de dependencias:

```bash
pip install -r requirements.txt
```


- Python 3.8 o superior
- Pygame (`pip install pygame`)
- PyInstaller (para empaquetar: `pip install pyinstaller`)

---

## ⚙️ Configuración (`config.ini`)

📌 El archivo `config.ini` es **opcional**. Si no se encuentra, se usarán valores por defecto.

### 📍 Ubicaciones soportadas:
- `%APPDATA%\\bouncerino\\config.ini`
- Misma carpeta donde se encuentra el `.scr` o `.exe`

### 📄 Ejemplo de `config.ini`

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

### 🔍 Descripción de cada opción:

| Clave                     | Tipo    | Descripción                                                                 |
|--------------------------|---------|-----------------------------------------------------------------------------|
| `NOMBRE_SCREENSAVER`     | string  | Título de la ventana. También usado por el sistema si se instala como `.scr`. |
| `ANCHO_BASE`             | int     | Tamaño base (en píxeles) del logo principal.                               |
| `VELOCIDAD_REBOTE`       | int     | Velocidad del movimiento del logo principal.                               |
| `MAX_ELEMENTOS`          | int     | Cantidad máxima de elementos pequeños generados tras rebotes.              |
| `ARCHIVO_IMAGEN`         | string  | Nombre del archivo de imagen principal. Por defecto: `image.png`.          |
| `TIEMPO_ESPERA`          | int     | Tiempo entre frames en milisegundos. Valores más bajos = animación fluida. |
| `ROTACION_MINIS_ACTIVADA`| bool    | `True` para permitir que los elementos pequeños roten.                      |
| `VELOCIDAD_MINIS_ROTACION` | int  | Velocidad de rotación de los elementos pequeños (si está activado).        |
| `COLOR_FONDO`            | RGB     | Color de fondo en formato `"R, G, B"` (ejemplo: `0, 0, 0` para negro).      |
| `ARCHIVO_FONDO`          | string  | Imagen de fondo. Si está vacío o no se encuentra, se usará `COLOR_FONDO`.  |

## ▶️ Cómo correrlo en desarrollo

### 🪟 Modo ventana (desarrollo)
Podés ejecutar `bouncerino.py` con el argumento `--ventana` para que corra en modo **ventana**, en lugar de pantalla completa. Ideal para testeo:

```bash
python src/bouncerino.py --ventana
```

### 🤫 Modo silent (scripts .bat)
Los scripts `install.bat` y `uninstall.bat` aceptan el parámetro `-silent` o `/silent` para ejecutar sin mostrar mensajes ni pausar la consola.

```bash
install.bat -silent
uninstall.bat /silent
```


Si querés probar bouncerino directamente desde el código fuente:

### 🐍 Usando Python directamente

```bash
cd bouncerino
python src/bouncerino.py
```

## 📄 Usando el script run.bat

Si estás en Windows, podés ejecutar directamente:

```bash
run.bat
```
Este script ejecuta `src/bouncerino.py` sin necesidad de compilarlo, ideal para desarrollo o pruebas rápidas.

---

## 🔨 Cómo compilar (generar `.scr` para Windows)

Para generar el archivo `.scr` (protector de pantalla instalable en Windows), ejecutá:

```bash
build.bat
```
Este script hace lo siguiente:

- Usa **PyInstaller** para crear un archivo `.exe` a partir de `src/bouncerino.py`.
- Lo renombra automáticamente como `bouncerino.scr`.
- Lo deja en la carpeta `dist/`.

---

## 📥 Instalación (modo screensaver de Windows)

📌 Este screensaver está diseñado para funcionar en sistemas **Windows 7 o superior**. Las rutas del sistema (`%APPDATA%`, `%WINDIR%\\System32`) son específicas de Windows.

Para instalar bouncerino como protector de  (Debe ejecutarse como administrador):

```bash
install.bat
```
Este script:

- Copia `bouncerino.scr` a `%WINDIR%\System32` (requerido por Windows para que aparezca en la lista de protectores de pantalla).
- Crea una carpeta de recursos en `%APPDATA%\bouncerino\`.
- Copia allí los archivos necesarios:
  - [`config.ini`](src/config.ini)
  - [`image.png`](src/image.png)

> 🧠 Si el programa no encuentra estos archivos en `%APPDATA%`, intentará cargarlos desde la misma carpeta donde se encuentra el `.scr` o `.exe`.

---

## ❌ Desinstalación

Para desinstalar completamente bouncerino (Debe ejecutarse como administrador):

```bash
uninstall.bat
```
Este script:

- Elimina `bouncerino.scr` del directorio `System32`.
- Borra completamente la carpeta de configuración `%APPDATA%\bouncerino`, incluyendo:
  - `config.ini`
  - `image.png` u otros recursos personalizados

> ✅ El desinstalador es seguro: no borra nada fuera de las rutas usadas por la instalación.

---

## 🧠 Comportamiento

- El screensaver se cierra automáticamente si:
  - Se presiona cualquier tecla
  - Se hace clic con el mouse
  - Se detecta movimiento del mouse

- Si `config.ini` o `image.png` no se encuentran:
  - Se usan **valores por defecto**
  - Y una **imagen roja de reemplazo**

- Se puede personalizar:
  - El fondo de pantalla: color (`COLOR_FONDO`) o imagen (`ARCHIVO_FONDO`)
  - El comportamiento de rotación de los elementos secundarios

📌 Si no se encuentra el archivo especificado en `ARCHIVO_IMAGEN`, se mostrará una imagen de reemplazo: un cuadrado rojo del tamaño especificado, para indicar que la imagen original no está disponible.

---

