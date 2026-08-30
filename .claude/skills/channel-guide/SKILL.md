---
name: channel-guide
description: Audita y valida la configuración de Django Channels, el archivo asgi.py, los enrutadores de WebSockets y el código de los Consumers para asegurar estabilidad asíncrona.
disable-model-invocation: true
---

# Skill: Inspector Arquitectónico de Django Channels

Este skill analiza la configuración asíncrona (ASGI) de tu proyecto de Django, asegurando que los sockets estén bien conectados y libres de bloqueos de hilos de ejecución.

## 📥 Datos Requeridos
Claude, solicita al usuario:
1. El **nombre de la app** donde se están implementando los WebSockets.
2. Comprobar si el archivo `asgi.py` principal ya ha sido modificado.

## 🚀 Pasos de Ejecución

Claude, realiza las siguientes inspecciones técnicas en el entorno local:

### 1. Auditoría del Núcleo ASGI y Settings
- Abre el archivo `settings.py` global del proyecto.
- Verifica que la propiedad `ASGI_APPLICATION` esté definida apuntando correctamente al archivo del proyecto raíz (ej: `django_mastery.asgi.application`).
- Asegúrate de que la librería `channels` esté registrada al principio de la lista `INSTALLED_APPS`.

### 2. Validación de Enrutamiento (`routing.py`)
- Revisa el archivo `routing.py` dentro de la app o del proyecto raíz.
- Asegúrate de que las rutas utilicen `re_path` o `path` apuntando estrictamente a un consumidor usando el método `.as_asgi()` (ej: `path('ws/metricas/', consumers.MetricasConsumer.as_asgi())`).

### 3. Análisis de Consumidores (`consumers.py`)
- Abre el archivo `consumers.py` de la aplicación.
- Verifica si hereda de clases estables como `WebsocketConsumer` (síncrona para tareas ligeras) o `AsyncWebsocketConsumer` (asíncrona nativa).
- Confirma que los métodos fundamentales (`connect`, `disconnect`, `receive`) implementen un manejo de excepciones básico para no colapsar la conexión del cliente ante datos corruptos.

## 🏁 Resultado Esperado
Muestra un reporte técnico con viñetas confirmando que el protocolo ASGI está listo y mapeado adecuadamente, o provee las correcciones exactas en caso de encontrar desalineaciones.
