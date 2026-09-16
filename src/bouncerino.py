import configparser
import ctypes
from ctypes import wintypes
import logging
import os
import random
import sys

import pygame

# Configure logging
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)

# Default configuration values
VALORES_POR_DEFECTO = {
    "NOMBRE_SCREENSAVER": "Bouncerino",
    "ANCHO_BASE": "400",
    "VELOCIDAD_REBOTE": "3",
    "MAX_ELEMENTOS": "100",
    "ARCHIVO_IMAGEN": "image.png",
    "TIEMPO_ESPERA": "10",
    "ROTACION_CLONES": "True",
    "VELOCIDAD_CLONES_ROTACION": "3",
    "COLOR_FONDO": "0,0,0",
    "ARCHIVO_FONDO": "",
    "MODO_FONDO": "expandir"
}

# Paths
APPDATA_PATH = os.path.join(os.getenv("APPDATA", ""), "Bouncerino")
LOCAL_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

# Utility to find files: APPDATA > local
def buscar_archivo(nombre_archivo):
    for base in (APPDATA_PATH, LOCAL_PATH):
        ruta = os.path.join(base, nombre_archivo)
        if ruta and os.path.isfile(ruta):
            return ruta
    return None

# Load configuration
def cargar_configuracion():
    config = configparser.ConfigParser()
    ruta_cfg = buscar_archivo("config.ini")
    if not ruta_cfg:
        logging.warning("No se encontró config.ini. Usando valores por defecto.")
        return VALORES_POR_DEFECTO.copy()

    config.read(ruta_cfg)
    if 'CONFIG' not in config:
        logging.warning("Sección [CONFIG] ausente. Usando valores por defecto.")
        return VALORES_POR_DEFECTO.copy()

    valores = {}
    for k, v in VALORES_POR_DEFECTO.items():
        valores[k] = config['CONFIG'].get(k, v)
    return valores

config = cargar_configuracion()

# Helper to parse config entries
def get_config(key, cast=str):
    raw = config.get(key, VALORES_POR_DEFECTO[key])
    # Strip comments
    clean = raw.split(';', 1)[0].strip()
    try:
        return cast(clean)
    except Exception:
        logging.warning(f"Error convirtiendo '{key}'='{clean}'. Usando defecto '{VALORES_POR_DEFECTO[key]}'")
        return cast(VALORES_POR_DEFECTO[key])

# Read settings
NOMBRE_SCREENSAVER = get_config("NOMBRE_SCREENSAVER")
ANCHO_BASE = get_config("ANCHO_BASE", int)
VELOCIDAD_REBOTE = get_config("VELOCIDAD_REBOTE", int)
MAX_ELEMENTOS = get_config("MAX_ELEMENTOS", int)
ARCHIVO_IMAGEN = get_config("ARCHIVO_IMAGEN")
TIEMPO_ESPERA = get_config("TIEMPO_ESPERA", int)
ROTACION_CLONES = get_config("ROTACION_CLONES").lower() in ("true","1","yes")
VELOCIDAD_ROTACION = get_config("VELOCIDAD_CLONES_ROTACION", int)

# Parse color
try:
    COLOR_FONDO = tuple(int(c) for c in get_config("COLOR_FONDO").split(','))
    assert len(COLOR_FONDO) == 3
except Exception:
    logging.warning("COLOR_FONDO inválido. Usando negro.")
    COLOR_FONDO = (0,0,0)

ARCHIVO_FONDO = get_config("ARCHIVO_FONDO")
MODO_FONDO = get_config("MODO_FONDO").lower()

# Initialize Pygame modules
pygame.init()

# Determine display mode
MODO_VENTANA = "--ventana" in sys.argv

def obtener_area_virtual_pantallas():
    if os.name != "nt":
        return None

    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    left = user32.GetSystemMetrics(76)  # SM_XVIRTUALSCREEN
    top = user32.GetSystemMetrics(77)  # SM_YVIRTUALSCREEN
    width = user32.GetSystemMetrics(78)  # SM_CXVIRTUALSCREEN
    height = user32.GetSystemMetrics(79)  # SM_CYVIRTUALSCREEN

    if width <= 0 or height <= 0:
        return None

    return left, top, width, height

def obtener_rects_monitores(origen_x=0, origen_y=0):
    if os.name != "nt":
        return []

    rects = []

    monitor_enum_proc = ctypes.WINFUNCTYPE(
        wintypes.BOOL,
        wintypes.HMONITOR,
        wintypes.HDC,
        ctypes.POINTER(wintypes.RECT),
        wintypes.LPARAM,
    )

    def callback(_monitor, _dc, rect, _data):
        left = rect.contents.left - origen_x
        top = rect.contents.top - origen_y
        width = rect.contents.right - rect.contents.left
        height = rect.contents.bottom - rect.contents.top
        rects.append(pygame.Rect(left, top, width, height))
        return 1

    ctypes.windll.user32.EnumDisplayMonitors(0, 0, monitor_enum_proc(callback), 0)
    return rects

def escalar_cubrir(img, ancho, alto):
    w, h = img.get_size()
    factor = max(ancho / w, alto / h)
    nuevo_tamaño = (int(w * factor), int(h * factor))
    escalada = pygame.transform.smoothscale(img, nuevo_tamaño)
    return escalada, escalada.get_rect(center=(ancho // 2, alto // 2))

def crear_fondos(img, tamaño, modo, monitores):
    if modo == "duplicar" and monitores:
        fondos = []
        for monitor in monitores:
            fondo_monitor, rect = escalar_cubrir(img, monitor.width, monitor.height)
            rect.topleft = (monitor.left + rect.left, monitor.top + rect.top)
            fondos.append((fondo_monitor, rect, monitor))
        return modo, fondos

    if modo == "ajustar":
        fondo_ajustado, rect = escalar_cubrir(img, *tamaño)
        return modo, [(fondo_ajustado, rect, pygame.Rect(0, 0, *tamaño))]

    if modo == "repetir":
        return modo, img

    return "expandir", pygame.transform.smoothscale(img, tamaño)

# Create screen
try:
    monitores = []
    if MODO_VENTANA:
        flags = 0
        tamaño = (800, 600)
    else:
        area_virtual = obtener_area_virtual_pantallas()
        if area_virtual:
            left, top, width, height = area_virtual
            os.environ["SDL_VIDEO_WINDOW_POS"] = f"{left},{top}"
            flags = pygame.NOFRAME
            tamaño = (width, height)
            monitores = obtener_rects_monitores(left, top)
            logging.info(f"Area virtual de pantallas detectada: {area_virtual}.")
        else:
            flags = pygame.FULLSCREEN
            tamaño = (pygame.display.Info().current_w, pygame.display.Info().current_h)

    pantalla = pygame.display.set_mode(tamaño, flags)
    pygame.display.set_caption(NOMBRE_SCREENSAVER)
    logging.info(f"Modo {'ventana' if MODO_VENTANA else 'protector'} activado a {tamaño}.")
except pygame.error as e:
    logging.error(f"Error al inicializar pantalla: {e}. Intentando modo ventana 800x600.")
    tamaño = (800, 600)
    pantalla = pygame.display.set_mode(tamaño)

# Load background surface optional
fondo = None
if ARCHIVO_FONDO:
    ruta_fondo = buscar_archivo(ARCHIVO_FONDO)
    if ruta_fondo:
        try:
            img_fondo = pygame.image.load(ruta_fondo)
            img_fondo = img_fondo.convert()  # after display init
            fondo = crear_fondos(img_fondo, tamaño, MODO_FONDO, monitores)
            logging.info(f"Fondo cargado: {ruta_fondo}")
        except Exception as e:
            logging.warning(f"No se pudo cargar fondo '{ruta_fondo}': {e}")
    else:
        logging.warning(f"Archivo de fondo '{ARCHIVO_FONDO}' no encontrado.")

# Function to load sprite with fallback
def cargar_imagen(archivo, base):
    ruta = buscar_archivo(archivo)
    if not ruta:
        logging.warning(f"Imagen '{archivo}' no encontrada. Generando fallback.")
        surf = pygame.Surface((base,base), pygame.SRCALPHA)
        surf.fill((255,0,0,150))  # semitransparente
        return surf
    try:
        img = pygame.image.load(ruta)
        img = img.convert_alpha()
    except Exception as e:
        logging.error(f"Error cargando '{ruta}': {e}. Usando fallback.")
        img = pygame.Surface((base,base), pygame.SRCALPHA)
        img.fill((255,0,0,150))

    w,h = img.get_size()
    factor = base / max(w,h)
    return pygame.transform.smoothscale(img, (int(w*factor), int(h*factor)))

# Main logo
logo = cargar_imagen(ARCHIVO_IMAGEN, ANCHO_BASE)
logo_rect = logo.get_rect()
ANCHO, ALTO = pantalla.get_size()
logo_rect.topleft = (random.randint(0, ANCHO - logo_rect.width), random.randint(0, ALTO - logo_rect.height))

# Movement
vel_x = vel_y = VELOCIDAD_REBOTE

# Create bouncing elements
def crear_elemento(x,y):
    element_size = random.randint(50,150)
    img = cargar_imagen(ARCHIVO_IMAGEN, element_size)
    rect = img.get_rect(center=(x,y))
    vx = random.choice([-1,1])*random.randint(1,5)
    vy = random.choice([-1,1])*random.randint(1,5)
    rot = random.choice([-1,1])*VELOCIDAD_ROTACION if ROTACION_CLONES else 0
    return [img, rect, vx, vy, 0, rot]

elementos = []
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)
origen_mouse = pygame.mouse.get_pos()
running = True

# Main loop
while running:
    # Draw background
    if fondo:
        pantalla.fill(COLOR_FONDO)
        modo_fondo, datos_fondo = fondo
        if modo_fondo in ("ajustar", "duplicar"):
            for superficie, rect, area in datos_fondo:
                pantalla.set_clip(area)
                pantalla.blit(superficie, rect)
            pantalla.set_clip(None)
        elif modo_fondo == "repetir":
            fw, fh = datos_fondo.get_size()
            for x in range(0, ANCHO, fw):
                for y in range(0, ALTO, fh):
                    pantalla.blit(datos_fondo, (x, y))
        else:
            pantalla.blit(datos_fondo, (0,0))
    else:
        pantalla.fill(COLOR_FONDO)

    # Update and bounce logo
    logo_rect.x += vel_x
    logo_rect.y += vel_y
    if logo_rect.left <= 0 or logo_rect.right >= ANCHO:
        vel_x *= -1
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(*logo_rect.center))
    if logo_rect.top <= 0 or logo_rect.bottom >= ALTO:
        vel_y *= -1
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(*logo_rect.center))

    # Update clones
    for el in elementos:
        img, rect, vx, vy, ang, rot = el
        rect.x += vx; rect.y += vy; ang += rot
        if rect.left <= 0 or rect.right >= ANCHO: el[2] = -vx
        if rect.top <= 0 or rect.bottom >= ALTO: el[3] = -vy
        surf = pygame.transform.rotate(img, ang)
        pantalla.blit(surf, surf.get_rect(center=rect.center))
        el[4] = ang

    pantalla.blit(logo, logo_rect)
    pygame.display.flip()
    clock.tick(1000 // max(1, TIEMPO_ESPERA))

    # Event handling
    for ev in pygame.event.get():
        if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT) or \
           (ev.type==pygame.MOUSEMOTION and ev.pos!=origen_mouse):
            running = False

pygame.quit()
