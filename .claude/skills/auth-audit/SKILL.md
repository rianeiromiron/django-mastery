---
name: auth-audit
description: Audita los archivos de vistas y urls de Django para asegurar que los endpoints privados cuenten con la protección de autenticación correspondiente.
disable-model-invocation: true
---

# Skill: Auditor de Seguridad y Autenticación Django

Este skill inspecciona el código de Django buscando brechas de seguridad donde vistas privadas carezcan de control de acceso para usuarios registrados.

## 📥 Datos Requeridos
Claude, solicita al usuario especificar el archivo de vistas (`views.py`) o de rutas (`urls.py`) de la app que desea auditar.

## 🚀 Pasos de Execution

Claude, realiza el siguiente análisis de seguridad de forma autónoma:

### 1. Detección de Vistas Protegidas
- Analiza cada función o clase en el archivo `views.py`.
- Identifica si la vista es de carácter privado (ej: páneles de control, edición de datos, perfiles de usuario).
- Verifica la presencia del decorador `@login_required` para vistas basadas en funciones, o el mixin `LoginRequiredMixin` para vistas basadas en clases.

### 2. Auditoría en Capa de Plantillas
- Si la vista renderiza un HTML, revisa que dentro de la plantilla se utilice la validación lógica `{% if user.is_authenticated %}` para ocultar botones sensibles (como "Eliminar", "Editar" o "Crear") a los usuarios anónimos.

### 3. Reporte y Corrección
- Si detectas una vista privada desprotegida:
  - Inyecta la importación `from django.contrib.auth.decorators import login_required`.
  - Agrega el decorador `@login_required` sobre la función afectada.
  - Asegúrate de configurar la redirección automática agregando `LOGIN_URL = 'login'` si no está definida globalmente.

## 🏁 Resultado Esperado
Muestra una lista con las vistas analizadas, marcando con un estado VERDE las que están seguras y en ROJO las que estaban vulnerables y han sido corregidas por el skill.
