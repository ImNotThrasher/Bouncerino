# 📦 CHANGELOG – Bouncerino

Este archivo documenta los cambios realizados en cada versión de **bouncerino**.

---

## [v0.9.2] - 2026-02-09

### 🐛 Correcciones

#### Scripts de Instalación
- **Fix #5**: Habilitado el prompt de selección de directorio personalizado en `install.bat` y `uninstall.bat`
  - Anteriormente las líneas estaban comentadas y siempre se usaba el directorio predeterminado
  - Ahora el usuario puede elegir dónde instalar o especificar ENTER para usar `%WINDIR%\System32`

#### Renderizado de Fondo
- **Fix**: Escalado automático de la imagen de fondo al tamaño de la pantalla
  - La imagen de fondo ahora se escala correctamente usando `pygame.transform.scale()`
  - Soporta tanto imágenes más pequeñas como más grandes que la resolución de pantalla
  - Funciona correctamente en modo ventana y pantalla completa

#### Manejo de Errores
- **Fix**: Actualización correcta de la variable `tamaño` en el bloque de manejo de errores
  - Cuando falla la inicialización de pantalla, la variable `tamaño` se actualiza antes de crear la pantalla de respaldo
  - Garantiza que el fondo se escale correctamente incluso cuando hay un error de inicialización

---

## [v0.9.1] - 2025-04-20

### 🔧 Instalación y Desinstalación
- Mensajes más claros en `install.bat` y `uninstall.bat` para indicar cada paso y resultado
- Manejo de errores robusto: validación de rutas, permisos y parámetros (`-silent`|`/silent`)
- Gestión centralizada de la configuración, respetando `%APPDATA%\Bouncerino` y la carpeta del ejecutable

### 🏗️ Script de Build
- Mejora en la gestión de variables (paths, nombres de archivo, versiones)
- Limpieza automática de artefactos de compilaciones anteriores antes de empaquetar

### 🔄 Refactorización del Script Principal
- Código reorganizado en funciones modulares para facilitar la lectura y el mantenimiento
- Documentación inline y comentarios que describen el flujo de ejecución

### ⚙️ Configuración
- Ajustes en `config.ini` para favorecer la legibilidad (comentarios explicativos, formato consistente)
- Validación de valores al iniciar (ancho, velocidad, colores), con avisos claros en caso de configuración inválida

### 📚 Documentación y Paquete
- Inclusión de todos los archivos necesarios en la release (`LICENSE`, `README.md` actualizado)
- Actualización de la sección de instalación/desinstalación en la documentación para reflejar los nuevos parámetros y mejoras

---

## [v0.9.0] - 2025-04-06

🆕 Primer release público del proyecto.

### Agregado
- Logo rebotando en pantalla completa
- Clones pequeños al rebotar, con rotación opcional
- Configuración editable vía `config.ini`
- Imagen personalizada (`image.png`)
- Fondo sólido o imagen de fondo
- Scripts `.bat` para:
  - Ejecutar (`run.bat`)
  - Compilar a `.scr` (`build.bat`)
  - Instalar y desinstalar (`install.bat`, `uninstall.bat`)
- Modo ventana para testing (`--ventana`)
- Soporte para instalación silenciosa (`-silent`)
- Valores por defecto si no hay config o imagen
- Licencia MIT incluida
