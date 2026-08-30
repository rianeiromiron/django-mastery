---
name: make-model
description: Genera el código de un modelo de Django y su registro en admin.py basándose en los campos que indique el usuario.
disable-model-invocation: true
---

# Skill: Generador Eficiente de Modelos Django

Este skill automatiza la creación de modelos en el ORM de Django dentro de una app específica y los registra en el panel de administración.

## 📥 Datos Requeridos
Claude, antes de proceder, debes asegurarte de que el usuario te proporcione:
1. El **nombre de la app** donde se creará el modelo.
2. El **nombre del modelo** (en Singular y CamelCase, ej: `Tarea` o `Articulo`).
3. La **lista de campos** con sus respectivos tipos de datos.

## 🚀 Pasos de Ejecución

Claude, ejecuta las siguientes acciones de forma autónoma:

### 1. Inyección de Código en `models.py`
- Abre el archivo `models.py` de la app indicada.
- Conserva los imports existentes (asegura `from django.db import models`).
- Define la clase del modelo heredando de `models.Model`.
- Agrega los campos solicitados utilizando las mejores prácticas de Django:
  - `CharField`: Define siempre un `max_length`.
  - `TextField`: Para textos largos, descripciones o notas.
  - `BooleanField`: Configura un `default` lógico (ej. `False`).
  - `DateTimeField`: Usa `auto_now_add=True` para fechas de creación.
- Implementa siempre el método mágico `__str__(self)` para que retorne una cadena legible que identifique al objeto (ej: el título).

### 2. Registro en `admin.py`
- Abre el archivo `admin.py` de la misma app.
- Importa el nuevo modelo.
- Regístralo utilizando el decorador moderno `@admin.register(NombreModelo)`.
- Crea una clase de administración personalizada que herede de `admin.ModelAdmin` e incluya el atributo `list_display` con las columnas clave para que sea vistoso en el panel de control.

### 3. Ejecución de Migraciones
- Corre el comando `python manage.py makemigrations` en la terminal para detectar el nuevo modelo.
- Corre el comando `python manage.py migrate` para impactar los cambios en la base de datos local (SQLite).

## 🏁 Resultado Esperado
Muestra al usuario las líneas de código agregadas a `models.py` y `admin.py`, y confirma que las migraciones se aplicaron con éxito sin errores en la consola.
