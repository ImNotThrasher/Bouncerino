import pygame
import random
import os
import configparser
import sys

# Inicializar Pygame
pygame.init()

# Ruta base de datos de recursos
APPDATA_PATH = os.path.join(os.getenv("APPDATA"), "bouncerino")
LOCAL_PATH = os.path.dirname(os.path.abspath(sys.argv[0]))

# Función para buscar archivo con prioridad: APPDATA > misma carpeta
def buscar_archivo(nombre_archivo):
    ruta_appdata = os.path.join(APPDATA_PATH, nombre_archivo)
    if os.path.exists(ruta_appdata):
        return ruta_appdata
    ruta_local = os.path.join(LOCAL_PATH, nombre_archivo)
    if os.path.exists(ruta_local):
        return ruta_local
    return None

# Función para cargar configuración desde archivo
def cargar_configuracion():
    config = configparser.ConfigParser()
    archivo_config = buscar_archivo("config.ini")

    valores_por_defecto = {
        "NOMBRE_SCREENSAVER": "bouncerino",
        "ANCHO_BASE": "400",
        "VELOCIDAD_REBOTE": "3",
        "MAX_ELEMENTOS": "100",
        "ARCHIVO_IMAGEN": "image.png",
        "TIEMPO_ESPERA": "10",
        "ROTACION_CLONES_ACTIVADA": "True",
        "VELOCIDAD_CLONES_ROTACION": "3",
        "COLOR_FONDO": "0, 0, 0",
        "ARCHIVO_FONDO": ""
    }

    if not archivo_config:
        print("⚠️ No se encontró config.ini. Usando configuración por defecto.")
        return valores_por_defecto

    config.read(archivo_config)

    if "CONFIG" not in config:
        print("⚠️ El archivo config.ini no contiene la sección [CONFIG]. Usando configuración por defecto.")
        return valores_por_defecto

    return {key: config["CONFIG"].get(key, valores_por_defecto[key]) for key in valores_por_defecto}

# Cargar configuración
config = cargar_configuracion()

# Función utilitaria para obtener valores con cast y limpieza
def get_config(key, default=None, cast=str):
    try:
        raw_value = config.get(key, default)
        cleaned = raw_value.partition(';')[0].strip()
        return cast(cleaned)
    except Exception:
        print(f"⚠️ Error en config: {key}. Usando valor por defecto: {default}")
        return default

# Asignar valores desde configuración
NOMBRE_SCREENSAVER = get_config("NOMBRE_SCREENSAVER", "bouncerino")
ANCHO_BASE = get_config("ANCHO_BASE", 400, int)
VELOCIDAD_REBOTE = get_config("VELOCIDAD_REBOTE", 3, int)
MAX_ELEMENTOS = get_config("MAX_ELEMENTOS", 100, int)
ARCHIVO_IMAGEN = get_config("ARCHIVO_IMAGEN", "image.png")
TIEMPO_ESPERA = get_config("TIEMPO_ESPERA", 10, int)
ROTACION_CLONES_ACTIVADA = get_config("ROTACION_CLONES_ACTIVADA", "True").lower() in ("true", "1", "yes")
VELOCIDAD_CLONES_ROTACION = get_config("VELOCIDAD_CLONES_ROTACION", 3, int)

try:
    COLOR_FONDO = tuple(map(int, get_config("COLOR_FONDO", "0, 0, 0").split(',')))
    if len(COLOR_FONDO) != 3:
        raise ValueError
except ValueError:
    print("⚠️ COLOR_FONDO inválido. Usando negro por defecto.")
    COLOR_FONDO = (0, 0, 0)

ARCHIVO_FONDO = get_config("ARCHIVO_FONDO", "")

# Cargar fondo desde archivo si se especifica
fondo_imagen = None
ruta_fondo = buscar_archivo(ARCHIVO_FONDO)
if ARCHIVO_FONDO and ruta_fondo:
    fondo_imagen = pygame.image.load(ruta_fondo).convert()

# Obtener tamaño de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h

# Soporte para modo ventana con "--ventana"
MODO_TEST = "--ventana" in sys.argv
pantalla = pygame.display.set_mode((800, 600) if MODO_TEST else (ANCHO, ALTO), pygame.FULLSCREEN if not MODO_TEST else 0)
pygame.display.set_caption(NOMBRE_SCREENSAVER)

# Función para cargar imagen con fallback
def cargar_imagen(archivo, tamano_base):
    ruta = buscar_archivo(archivo)
    if not ruta:
        print(f"⚠️ No se encontró la imagen: {archivo}. Usando imagen de reemplazo.")
        imagen = pygame.Surface((tamano_base, tamano_base), pygame.SRCALPHA)
        imagen.fill((255, 0, 0))
        return imagen
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
    except pygame.error:
        print(f"❌ Error al cargar la imagen: {ruta}. Usando imagen de reemplazo.")
        imagen = pygame.Surface((tamano_base, tamano_base), pygame.SRCALPHA)
        imagen.fill((255, 0, 0))
        return imagen

    ancho_original, alto_original = imagen.get_size()
    escala = tamano_base / max(ancho_original, alto_original)
    return pygame.transform.scale(imagen, (int(ancho_original * escala), int(alto_original * escala)))

# Cargar imagen principal
logo = cargar_imagen(ARCHIVO_IMAGEN, ANCHO_BASE)
logo_rect = logo.get_rect()
logo_rect.x = random.randint(0, ANCHO - logo_rect.width)
logo_rect.y = random.randint(0, ALTO - logo_rect.height)

# Movimiento
vel_x, vel_y = VELOCIDAD_REBOTE, VELOCIDAD_REBOTE
elementos = []

# Crear clones
def crear_elemento(x, y):
    tamano = random.randint(50, 150)
    imagen_pequenio = cargar_imagen(ARCHIVO_IMAGEN, tamano)
    rect = imagen_pequenio.get_rect(topleft=(x, y))
    vel_x = random.choice([-1, 1]) * random.randint(1, 5)
    vel_y = random.choice([-1, 1]) * random.randint(1, 5)
    angulo = 0
    rotacion = random.choice([-1, 1]) * VELOCIDAD_CLONES_ROTACION if ROTACION_CLONES_ACTIVADA else 0
    return [imagen_pequenio, rect, vel_x, vel_y, angulo, rotacion]

# Loop principal
ejecutando = True
pygame.mouse.set_visible(False)
posicion_mouse_inicial = pygame.mouse.get_pos()
clock = pygame.time.Clock()

while ejecutando:
    pantalla.blit(fondo_imagen, (0, 0)) if fondo_imagen else pantalla.fill(COLOR_FONDO)

    logo_rect.x += vel_x
    logo_rect.y += vel_y

    if logo_rect.left <= 0 or logo_rect.right >= ANCHO:
        vel_x = -vel_x
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(*logo_rect.center))
    if logo_rect.top <= 0 or logo_rect.bottom >= ALTO:
        vel_y = -vel_y
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(*logo_rect.center))

    for e in elementos:
        imagen, rect, vx, vy, angulo, rotacion = e
        rect.x += vx
        rect.y += vy
        angulo += rotacion

        if rect.left <= 0 or rect.right >= ANCHO:
            e[2] = -vx
        if rect.top <= 0 or rect.bottom >= ALTO:
            e[3] = -vy

        imagen_rotada = pygame.transform.rotate(imagen, angulo)
        nuevo_rect = imagen_rotada.get_rect(center=rect.center)
        pantalla.blit(imagen_rotada, nuevo_rect)
        e[4] = angulo

    pantalla.blit(logo, logo_rect)
    pygame.display.flip()
    clock.tick(1000 // TIEMPO_ESPERA)

    for event in pygame.event.get():
        if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT) or \
           (event.type == pygame.MOUSEMOTION and event.pos != posicion_mouse_inicial):
            ejecutando = False

pygame.quit()
