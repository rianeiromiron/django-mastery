---
name: gen-api
description: Genera automáticamente la infraestructura de Django REST Framework (Serializadores, ViewSets y URLs) a partir de un modelo existente.
disable-model-invocation: true
---

# Skill: Generador de APIs con Django REST Framework

Este skill automatiza la conversión de un modelo estándar de Django en un endpoint de API REST compatible con JSON empleando DRF.

## 📥 Datos Requeridos
Claude, solicita al usuario:
1. El **nombre de la app** donde se creará la API.
2. El **nombre del modelo** que se desea exponer a través de la API.

## 🚀 Pasos de Ejecución

Claude, realiza las siguientes tareas en tu entorno local:

### 1. Instalación de Dependencias
- Verifica si `djangorestframework` está listado en tu `requirements.txt`.
- Si no está, ejecutan `pip install djangorestframework` y actualiza el archivo `requirements.txt`.
- Agrega `'rest_framework',` a la lista `INSTALLED_APPS` dentro del archivo `settings.py` global.

### 2. Creación del Serializador (`serializers.py`)
- Crea un archivo llamado `serializers.py` dentro de la app indicada.
- Importa `serializers` de `rest_framework` y el modelo especificado por el usuario.
- Define una clase que herede de `serializers.ModelSerializer`.
- Configura la subclase `Meta` especificando el modelo y definiendo `fields = '__all__'`.

### 3. Configuración de Vistas y Rutas de API
- Abre `views.py` de la app e importa `viewsets` de `rest_framework` junto al modelo y su nuevo serializador.
- Crea una clase que herede de `viewsets.ModelViewSet`, asignando el `queryset` completo y el `serializer_class`.
- Crea un archivo `urls.py` dentro de la app, configura un `DefaultRouter` de DRF, registra el ViewSet y añade las rutas generadas al patrón de URLs. Asegúrate de incluir estas rutas en el archivo `urls.py` maestro del proyecto.

## 🏁 Resultado Esperado
Confirma la correcta instalación de la librería y muestra la estructura de código JSON generada para los nuevos endpoints de la API.
