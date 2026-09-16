from __future__ import annotations

import configparser
import ctypes
from ctypes import wintypes
from dataclasses import dataclass
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


@dataclass
class Config:
    nombre_screensaver: str
    ancho_base: int
    velocidad_rebote: int
    max_elementos: int
    archivo_imagen: str
    tiempo_espera: int
    rotacion_clones: bool
    velocidad_rotacion: int
    color_fondo: tuple[int, int, int]
    archivo_fondo: str
    modo_fondo: str


def buscar_archivo(nombre_archivo):
    for base in (APPDATA_PATH, LOCAL_PATH):
        ruta = os.path.join(base, nombre_archivo)
        if ruta and os.path.isfile(ruta):
            return ruta
    return None


def cargar_configuracion_base():
    parser = configparser.ConfigParser()
    ruta_cfg = buscar_archivo("config.ini")
    if not ruta_cfg:
        logging.warning("No se encontró config.ini. Usando valores por defecto.")
        return VALORES_POR_DEFECTO.copy()

    parser.read(ruta_cfg)
    if 'CONFIG' not in parser:
        logging.warning("Sección [CONFIG] ausente. Usando valores por defecto.")
        return VALORES_POR_DEFECTO.copy()

    valores = {}
    for key, value in VALORES_POR_DEFECTO.items():
        valores[key] = parser['CONFIG'].get(key, value)
    return valores


def get_config(config, key, cast=str):
    raw = config.get(key, VALORES_POR_DEFECTO[key])
    clean = raw.split(';', 1)[0].strip()
    try:
        return cast(clean)
    except Exception:
        logging.warning(f"Error convirtiendo '{key}'='{clean}'. Usando defecto '{VALORES_POR_DEFECTO[key]}'")
        return cast(VALORES_POR_DEFECTO[key])


def parsear_bool(valor):
    return valor.lower() in ("true", "1", "yes")


def parsear_color(config):
    try:
        color = tuple(int(c) for c in get_config(config, "COLOR_FONDO").split(','))
        assert len(color) == 3
        return color
    except Exception:
        logging.warning("COLOR_FONDO inválido. Usando negro.")
        return (0, 0, 0)


def cargar_configuracion():
    config = cargar_configuracion_base()
    return Config(
        nombre_screensaver=get_config(config, "NOMBRE_SCREENSAVER"),
        ancho_base=get_config(config, "ANCHO_BASE", int),
        velocidad_rebote=get_config(config, "VELOCIDAD_REBOTE", int),
        max_elementos=get_config(config, "MAX_ELEMENTOS", int),
        archivo_imagen=get_config(config, "ARCHIVO_IMAGEN"),
        tiempo_espera=get_config(config, "TIEMPO_ESPERA", int),
        rotacion_clones=parsear_bool(get_config(config, "ROTACION_CLONES")),
        velocidad_rotacion=get_config(config, "VELOCIDAD_CLONES_ROTACION", int),
        color_fondo=parsear_color(config),
        archivo_fondo=get_config(config, "ARCHIVO_FONDO"),
        modo_fondo=get_config(config, "MODO_FONDO").lower(),
    )


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


def crear_pantalla(config, modo_ventana):
    try:
        monitores = []
        if modo_ventana:
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
        pygame.display.set_caption(config.nombre_screensaver)
        logging.info(f"Modo {'ventana' if modo_ventana else 'protector'} activado a {tamaño}.")
        return pantalla, tamaño, monitores
    except pygame.error as e:
        logging.error(f"Error al inicializar pantalla: {e}. Intentando modo ventana 800x600.")
        tamaño = (800, 600)
        return pygame.display.set_mode(tamaño), tamaño, []


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


def cargar_fondo(config, tamaño, monitores):
    if not config.archivo_fondo:
        return None

    ruta_fondo = buscar_archivo(config.archivo_fondo)
    if not ruta_fondo:
        logging.warning(f"Archivo de fondo '{config.archivo_fondo}' no encontrado.")
        return None

    try:
        img_fondo = pygame.image.load(ruta_fondo)
        img_fondo = img_fondo.convert()
        fondo = crear_fondos(img_fondo, tamaño, config.modo_fondo, monitores)
        logging.info(f"Fondo cargado: {ruta_fondo}")
        return fondo
    except Exception as e:
        logging.warning(f"No se pudo cargar fondo '{ruta_fondo}': {e}")
        return None


def dibujar_fondo(pantalla, fondo, color_fondo, ancho, alto):
    if not fondo:
        pantalla.fill(color_fondo)
        return

    pantalla.fill(color_fondo)
    modo_fondo, datos_fondo = fondo
    if modo_fondo in ("ajustar", "duplicar"):
        for superficie, rect, area in datos_fondo:
            pantalla.set_clip(area)
            pantalla.blit(superficie, rect)
        pantalla.set_clip(None)
    elif modo_fondo == "repetir":
        fw, fh = datos_fondo.get_size()
        for x in range(0, ancho, fw):
            for y in range(0, alto, fh):
                pantalla.blit(datos_fondo, (x, y))
    else:
        pantalla.blit(datos_fondo, (0, 0))


def cargar_imagen(archivo, base):
    ruta = buscar_archivo(archivo)
    if not ruta:
        logging.warning(f"Imagen '{archivo}' no encontrada. Generando fallback.")
        surf = pygame.Surface((base, base), pygame.SRCALPHA)
        surf.fill((255, 0, 0, 150))
        return surf
    try:
        img = pygame.image.load(ruta)
        img = img.convert_alpha()
    except Exception as e:
        logging.error(f"Error cargando '{ruta}': {e}. Usando fallback.")
        img = pygame.Surface((base, base), pygame.SRCALPHA)
        img.fill((255, 0, 0, 150))

    w, h = img.get_size()
    factor = base / max(w, h)
    return pygame.transform.smoothscale(img, (int(w * factor), int(h * factor)))


def crear_logo(config, ancho, alto):
    logo = cargar_imagen(config.archivo_imagen, config.ancho_base)
    logo_rect = logo.get_rect()
    logo_rect.topleft = (
        random.randint(0, ancho - logo_rect.width),
        random.randint(0, alto - logo_rect.height),
    )
    return logo, logo_rect


def crear_elemento(config, x, y):
    element_size = random.randint(50, 150)
    img = cargar_imagen(config.archivo_imagen, element_size)
    rect = img.get_rect(center=(x, y))
    vx = random.choice([-1, 1]) * random.randint(1, 5)
    vy = random.choice([-1, 1]) * random.randint(1, 5)
    rot = random.choice([-1, 1]) * config.velocidad_rotacion if config.rotacion_clones else 0
    return [img, rect, vx, vy, 0, rot]


def actualizar_logo(config, logo_rect, elementos, ancho, alto, vel_x, vel_y):
    logo_rect.x += vel_x
    logo_rect.y += vel_y
    if logo_rect.left <= 0 or logo_rect.right >= ancho:
        vel_x *= -1
        if len(elementos) < config.max_elementos:
            elementos.append(crear_elemento(config, *logo_rect.center))
    if logo_rect.top <= 0 or logo_rect.bottom >= alto:
        vel_y *= -1
        if len(elementos) < config.max_elementos:
            elementos.append(crear_elemento(config, *logo_rect.center))
    return vel_x, vel_y


def actualizar_y_dibujar_clones(pantalla, elementos, ancho, alto):
    for el in elementos:
        img, rect, vx, vy, ang, rot = el
        rect.x += vx
        rect.y += vy
        ang += rot
        if rect.left <= 0 or rect.right >= ancho:
            el[2] = -vx
        if rect.top <= 0 or rect.bottom >= alto:
            el[3] = -vy
        surf = pygame.transform.rotate(img, ang)
        pantalla.blit(surf, surf.get_rect(center=rect.center))
        el[4] = ang


def debe_salir(origen_mouse):
    for ev in pygame.event.get():
        if ev.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.QUIT):
            return True
        if ev.type == pygame.MOUSEMOTION and ev.pos != origen_mouse:
            return True
    return False


def ejecutar_loop(pantalla, config, fondo):
    logo, logo_rect = crear_logo(config, *pantalla.get_size())
    ancho, alto = pantalla.get_size()
    vel_x = vel_y = config.velocidad_rebote
    elementos = []
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(False)
    origen_mouse = pygame.mouse.get_pos()

    running = True
    while running:
        dibujar_fondo(pantalla, fondo, config.color_fondo, ancho, alto)

        vel_x, vel_y = actualizar_logo(
            config,
            logo_rect,
            elementos,
            ancho,
            alto,
            vel_x,
            vel_y,
        )

        actualizar_y_dibujar_clones(pantalla, elementos, ancho, alto)
        pantalla.blit(logo, logo_rect)
        pygame.display.flip()
        clock.tick(1000 // max(1, config.tiempo_espera))

        if debe_salir(origen_mouse):
            running = False


def main():
    config = cargar_configuracion()
    modo_ventana = "--ventana" in sys.argv

    pygame.init()
    pantalla, tamaño, monitores = crear_pantalla(config, modo_ventana)
    fondo = cargar_fondo(config, tamaño, monitores)
    ejecutar_loop(pantalla, config, fondo)
    pygame.quit()


if __name__ == "__main__":
    main()
