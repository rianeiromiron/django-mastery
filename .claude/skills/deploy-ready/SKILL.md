---
name: deploy-ready
description: Audita las configuraciones de seguridad de Django para producción y genera automáticamente los archivos de dockerización (Dockerfile y docker-compose.yml) para el despliegue del proyecto en contenedores.
disable-model-invocation: true
---

# Skill: Certificador de Despliegue e Infraestructura Docker

Este skill inspecciona el proyecto de Django antes de ir a producción, parchando brechas críticas de seguridad en settings.py y montando la arquitectura de contenedores Docker.

## 📥 Datos Requeridos
Claude, antes de proceder, confirma con el usuario que el proyecto compile de forma local y que cuente con un archivo `requirements.txt` actualizado.

## 🚀 Pasos de Ejecución

Claude, ejecuta las siguientes directrices de ingeniería de infraestructura de forma autónoma:

### 1. Auditoría de Seguridad de Producción (`settings.py`)
- Escanea el archivo `settings.py` global y verifica que:
  - `DEBUG` evalúe estrictamente a `False` si la variable de entorno está apagada.
  - No existan llaves o contraseñas quemadas físicamente en el texto.
  - Recomienda configuraciones de cookies seguras (`SECURE_SSL_REDIRECT = True`, `SESSION_COOKIE_SECURE = True`).

### 2. Generación del Entorno de Contenedores (`Dockerfile`)
- En la raíz del proyecto, crea un archivo llamado `Dockerfile` (sin extensión) utilizando una imagen base ligera de Python (ej: `python:3.11-slim`).
- Configura las instrucciones para:
  - Definir las variables de entorno de Python (`PYTHONTONTWRITEBYTECODE=1`, `PYTHONUNBUFFERED=1`).
  - Establecer el directorio de trabajo en `/app`.
  - Instalar dependencias mediante el archivo `requirements.txt`.
  - Copiar todo el código fuente del proyecto al contenedor.

### 3. Orquestación Multi-Servicio (`docker-compose.yml`)
- Crea un archivo `docker-compose.yml` en la raíz que orqueste:
  - El servicio web de Django corriendo a través de un servidor de producción (como `gunicorn` o `daphne` para manejar tus WebSockets del proyecto 7).
  - El servicio del broker de mensajes de Redis (necesario para Celery del proyecto 8).
  - Configura los volúmenes de persistencia para los archivos estáticos y la base de datos.

## 🏁 Resultado Esperado
Muestra los archivos Docker generados y un resumen de las recomendaciones de seguridad aplicadas para garantizar un despliegue exitoso en la nube.
