---
name: init-django
description: Automatiza la creación y configuración inicial de un entorno de desarrollo profesional para un nuevo proyecto de Django.
---

# Skill: Inicialización Estándar de Django

Este skill guía a Claude Code para configurar un entorno limpio, seguro y estructurado para un nuevo proyecto de Django, siguiendo las mejores prácticas de la industria.

## 📋 Requisitos Previos
- Tener Python 3.10 o superior instalado en el sistema.
- Estar en el directorio raíz donde se desea crear el proyecto.

## 🚀 Pasos de Ejecución

Claude, debes ejecutar y verificar los siguientes pasos de forma secuencial:

### 1. Entorno Virtual y Dependencias
- Crea un entorno virtual de Python llamado `.venv`.
- Activa el entorno virtual según el sistema operativo actual.
- Actualiza `pip`.
- Instala `django` y `python-dotenv` (para manejar variables de entorno).
- Genera el archivo `requirements.txt` con las versiones congeladas.

### 2. Estructura del Proyecto Django
- Pregunta al usuario el **nombre del proyecto** y el **nombre de la primera app** (por ejemplo, `core` o `blog`).
- Ejecuta `django-admin startproject <nombre_proyecto> .` (usa el punto al final para evitar carpetas anidadas repetitivas).
- Ejecuta `python manage.py startapp <nombre_app>`.

### 3. Configuración de Archivos Base
- Crea un archivo `.env` en la raíz con:
  - `DEBUG=True`
  - `SECRET_KEY=` (Genera una clave aleatoria segura de 50 caracteres).
- Crea un archivo `.gitignore` estándar para Python y Django (incluyendo `.venv/`, `*.pyc`, `db.sqlite3`, y `.env`).
- Configura el archivo `settings.py` para:
  - Importar `os` y `dotenv` al inicio para cargar el archivo `.env`.
  - Reemplazar la `SECRET_KEY` física por `os.getenv('SECRET_KEY')`.
  - Reemplazar `DEBUG = True` por `os.getenv('DEBUG', 'False') == 'True'`.
  - Registrar la nueva app en la lista `INSTALLED_APPS`.
  - Configurar las rutas para archivos estáticos (`STATIC_URL`, `STATICFILES_DIRS`, `STATIC_ROOT`).

### 4. Verificación Inicial
- Ejecuta `python manage.py migrate` para aplicar las migraciones iniciales de Django.
- Ejecuta `python manage.py check` para comprobar que no existan errores de configuración.

## 🏁 Resultado Esperado
Al finalizar, muestra un resumen con la estructura de carpetas generada y confirma que el servidor de desarrollo está listo para correr con `python manage.py runserver`.
