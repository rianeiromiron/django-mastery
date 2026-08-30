---
name: orm-wizard
description: Analiza las consultas del ORM de Django en un archivo de vistas para optimizar el rendimiento, corregir el problema N+1 y sugerir filtros avanzados.
disable-model-invocation: true
---

# Skill: Mago del ORM de Django

Este skill audita el rendimiento y la lógica de las consultas a bases de datos en los archivos de vistas (`views.py`) de Django.

## 📥 Datos Requeridos
Claude, solicita al usuario la ruta del archivo de vistas que desea auditar (ej: `gestor_tareas/views.py` o la nueva app que se cree).

## 🚀 Pasos de Ejecución

Claude, ejecuta las siguientes acciones de forma analítica:

### 1. Auditoría de Rendimiento (Anti N+1)
- Revisa las consultas del archivo buscando bucles que llamen a atributos de modelos relacionados con Llaves Foráneas (`ForeignKey`) o relaciones Muchos a Muchos (`ManyToManyField`).
- Si detectas ineficiencias, reescribe la consulta utilizando:
  - `select_related(*campos)` para relaciones directas (ForeignKey).
  - `prefetch_related(*campos)` para relaciones inversas o ManyToMany.

### 2. Implementación de Búsquedas Inteligentes
- Si el usuario te pide añadir un buscador, asegúrate de importar `from django.db.models import Q`.
- Configura la consulta usando `Q(campo__icontains=query) | Q(segundo_campo__icontains=query)` para búsquedas parciales e insensibles a mayúsculas.

### 3. Paginación Robusta
- Verifica que el listado de elementos incluya el módulo `from django.core.paginator import Paginator`.
- Reestructura la vista para limitar los resultados por página (ej: 10 por página) y capturar excepciones de páginas vacías o no numéricas.

## 🏁 Resultado Esperado
Muestra una comparativa del código original vs el código optimizado, explicando brevemente cuántas consultas a la base de datos se ahorraron con la optimización.
