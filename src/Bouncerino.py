import pygame
import random
import os
import configparser
import sys

# Inicializar Pygame
pygame.init()

# Ruta base de datos de recursos
APPDATA_PATH = os.path.join(os.getenv("APPDATA"), "Bouncerino")
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
        "NOMBRE_SCREENSAVER": "Bouncerino",
        "ANCHO_BASE": "400",
        "VELOCIDAD_REBOTE": "3",
        "MAX_ELEMENTOS": "100",
        "ARCHIVO_IMAGEN": "image.png",
        "TIEMPO_ESPERA": "10",
        "ROTACION_MINIS_ACTIVADA": "True",
        "VELOCIDAD_MINIS_ROTACION": "3",
        "COLOR_FONDO": "0, 0, 0",
        "ARCHIVO_FONDO": ""
    }

    if not archivo_config:
        print("⚠️ No se encontró config.ini. Usando configuración por defecto.")
        return valores_por_defecto

    config.read(archivo_config)
    return {key: config["CONFIG"].get(key, valores_por_defecto[key]) for key in valores_por_defecto}

# Cargar configuración
config = cargar_configuracion()

# Asignar valores desde configuración
NOMBRE_SCREENSAVER = config["NOMBRE_SCREENSAVER"]
ANCHO_BASE = int(config["ANCHO_BASE"])
VELOCIDAD_REBOTE = int(config["VELOCIDAD_REBOTE"])
MAX_ELEMENTOS = int(config["MAX_ELEMENTOS"])
ARCHIVO_IMAGEN = config["ARCHIVO_IMAGEN"]
TIEMPO_ESPERA = int(config["TIEMPO_ESPERA"])
ROTACION_MINIS_ACTIVADA = config["ROTACION_MINIS_ACTIVADA"].lower() == "true"
VELOCIDAD_MINIS_ROTACION = int(config["VELOCIDAD_MINIS_ROTACION"])
COLOR_FONDO = tuple(map(int, config["COLOR_FONDO"].split(',')))
ARCHIVO_FONDO = config["ARCHIVO_FONDO"]

# Cargar fondo desde archivo si se especifica
fondo_imagen = None
ruta_fondo = buscar_archivo(ARCHIVO_FONDO)
if ARCHIVO_FONDO and ruta_fondo:
    fondo_imagen = pygame.image.load(ruta_fondo).convert()

# Obtener tamaño de la pantalla
info_pantalla = pygame.display.Info()
ANCHO, ALTO = info_pantalla.current_w, info_pantalla.current_h

# Configurar pantalla completa
pantalla = pygame.display.set_mode((ANCHO, ALTO), pygame.FULLSCREEN)
pygame.display.set_caption(NOMBRE_SCREENSAVER)

# Función para cargar la imagen con soporte para PNG, JPG, etc.
def cargar_imagen(archivo, tamano_base):
    ruta = buscar_archivo(archivo)
    if not ruta:
        print(f"⚠️ No se encontró la imagen: {archivo}. Usando imagen de reemplazo.")
        imagen = pygame.Surface((tamano_base, tamano_base), pygame.SRCALPHA)
        imagen.fill((255, 0, 0))  # Rojo de error
        return imagen
    try:
        imagen = pygame.image.load(ruta).convert_alpha()
    except pygame.error:
        print(f"❌ Error al cargar la imagen: {ruta}. Usando imagen de reemplazo.")
        imagen = pygame.Surface((tamano_base, tamano_base), pygame.SRCALPHA)
        imagen.fill((255, 0, 0))  # Rojo de error
        return imagen

    ancho_original, alto_original = imagen.get_size()
    escala = tamano_base / max(ancho_original, alto_original)
    return pygame.transform.scale(imagen, (int(ancho_original * escala), int(alto_original * escala)))

# Cargar la imagen principal
logo = cargar_imagen(ARCHIVO_IMAGEN, ANCHO_BASE)
logo_rect = logo.get_rect()

# Posición inicial aleatoria
logo_rect.x = random.randint(0, ANCHO - logo_rect.width)
logo_rect.y = random.randint(0, ALTO - logo_rect.height)

# Velocidad de movimiento
vel_x, vel_y = VELOCIDAD_REBOTE, VELOCIDAD_REBOTE

# Lista de elementos pequenios
elementos = []

# Función para crear elementos pequenios con rotación
def crear_elemento(x, y):
    tamano = random.randint(50, 150)
    imagen_pequenio = cargar_imagen(ARCHIVO_IMAGEN, tamano)
    rect_pequenio = imagen_pequenio.get_rect()
    rect_pequenio.x = x
    rect_pequenio.y = y
    vel_pequenio_x = random.choice([-1, 1]) * random.randint(1, 5)
    vel_pequenio_y = random.choice([-1, 1]) * random.randint(1, 5)
    angulo = 0
    vel_rotacion = random.choice([-1, 1]) * VELOCIDAD_MINIS_ROTACION if ROTACION_MINIS_ACTIVADA else 0
    return [imagen_pequenio, rect_pequenio, vel_pequenio_x, vel_pequenio_y, angulo, vel_rotacion]

# Bucle principal
ejecutando = True
pygame.mouse.set_visible(False)
posicion_mouse_inicial = pygame.mouse.get_pos()

while ejecutando:
    if fondo_imagen:
        pantalla.blit(fondo_imagen, (0, 0))
    else:
        pantalla.fill(COLOR_FONDO)

    logo_rect.x += vel_x
    logo_rect.y += vel_y

    if logo_rect.left <= 0 or logo_rect.right >= ANCHO:
        vel_x = -vel_x
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(logo_rect.centerx, logo_rect.centery))
    if logo_rect.top <= 0 or logo_rect.bottom >= ALTO:
        vel_y = -vel_y
        if len(elementos) < MAX_ELEMENTOS:
            elementos.append(crear_elemento(logo_rect.centerx, logo_rect.centery))

    for elemento in elementos:
        imagen, rect, vel_x, vel_y, angulo, vel_rotacion = elemento
        rect.x += vel_x
        rect.y += vel_y
        angulo += vel_rotacion

        if rect.left <= 0 or rect.right >= ANCHO:
            elemento[2] = -vel_x
        if rect.top <= 0 or rect.bottom >= ALTO:
            elemento[3] = -vel_y

        imagen_rotada = pygame.transform.rotate(imagen, angulo)
        nuevo_rect = imagen_rotada.get_rect(center=rect.center)
        pantalla.blit(imagen_rotada, nuevo_rect)
        elemento[4] = angulo

    pantalla.blit(logo, logo_rect)
    pygame.display.flip()
    pygame.time.delay(TIEMPO_ESPERA)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
            ejecutando = False
        elif event.type == pygame.MOUSEMOTION:
            if event.pos != posicion_mouse_inicial:
                ejecutando = False
        elif event.type == pygame.QUIT:
            ejecutando = False

pygame.quit()