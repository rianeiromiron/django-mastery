---
name: celery-worker
description: Audita las tareas en segundo plano creadas con Celery, asegurando la correcta importación de shared_task y el manejo adecuado de reintentos y excepciones.
disable-model-invocation: true
---

# Skill: Auditor de Tareas en Segundo Plano (Celery)

Este skill analiza el archivo `tasks.py` de cualquier aplicación de Django para certificar la estabilidad de los procesos pesados distribuidos en segundo plano.

## 📥 Datos Requeridos
Claude, solicita al usuario:
1. El **nombre de la app** donde se están registrando las tareas asíncronas.
2. Comprobar si Celery ya está instanciado en el proyecto raíz.

## 🚀 Pasos de Ejecución

Claude, realiza las siguientes inspecciones en el entorno del proyecto:

### 1. Verificación del Entorno Celery
- Revisa si existe el archivo `celery.py` junto a tu `settings.py` global encargado de inicializar la app de Celery y autocargar las tareas de las aplicaciones registradas.
- Verifica que el `settings.py` cuente con la variable `CELERY_BROKER_URL` apuntando a un servicio de almacenamiento como Redis (`redis://localhost:6379/0`).

### 2. Análisis de `tasks.py`
- Abre el archivo `tasks.py` de la aplicación indicada.
- Asegúrate de que cada función costosa en tiempo use el decorador `@shared_task`.
- Si la tarea realiza peticiones externas (como enviar correos o consumir APIs de terceros), exige la configuración de reintentos automáticos ante caídas de red: `@shared_task(bind=True, max_retries=3, default_retry_delay=60)`.

## 🏁 Resultado Esperado
Presenta un informe confirmando si la tarea está lista para ser enviada a la cola de trabajadores o añade los bloques `try/except` con llamadas de reintento en caso de riesgos de falla.
