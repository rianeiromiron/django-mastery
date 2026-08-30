---
name: htmx-ui
description: Diseña e implementa componentes reactivos en Django utilizando HTMX para peticiones dinámicas y clases de Tailwind CSS para el diseño visual.
disable-model-invocation: true
---

# Skill: Constructor de Interfaces Reactivas (HTMX + Tailwind)

Este skill guía a Claude Code para transformar vistas tradicionales de Django en componentes interactivos modernos que no requieren recargar la página.

## 📥 Datos Requeridos
Claude, solicita al usuario:
1. El **nombre de la app** donde se creará la interfaz interactiva.
2. El **componente que se desea hacer dinámico** (ej: un buscador en tiempo real, eliminación de elementos con un clic o un botón de me gusta).

## 🚀 Pasos de Ejecución

Claude, realiza las siguientes tareas de configuración e integración de forma autónoma:

### 1. Inyección de Librerías en el Template Base
- Abre tu plantilla global `base.html`.
- Si no están presentes, inyecta en la etiqueta `<head>` los scripts CDN oficiales de:
  - **Tailwind CSS:** `<script src="https://tailwindcss.com"></script>`
  - **HTMX:** `<script src="https://unpkg.com"></script>`

### 2. Estructura de Atributos HTMX
Al diseñar los formularios o botones dinámicos en la plantilla, implementa obligatoriamente:
- `hx-post` o `hx-get`: Para apuntar a la URL de Django de forma asíncrona.
- `hx-target`: Para especificar el ID del contenedor HTML (`#id-contenedor`) que debe actualizarse con la respuesta.
- `hx-swap`: Define el método de intercambio (ej: `innerHTML` para reemplazar el contenido o `beforeend` para añadir una fila al final).

### 3. Vistas de Respuestas Parciales en Django
- Abre el archivo `views.py` de la app elegida.
- Diseña vistas compactas que, al recibir una petición de HTMX, rendericen únicamente un bloque o archivo HTML de fragmento (ej: `fragmento_lista.html`) en lugar de extender la plantilla completa con `base.html`.

## 🏁 Resultado Esperado
Muestra el código HTML del componente reactivo enriquecido con Tailwind y confirma que la vista de Django está lista para procesar las peticiones AJAX en segundo plano.
