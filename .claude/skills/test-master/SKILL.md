---
name: test-master
description: Analiza las vistas y modelos de Django de una aplicación para generar automáticamente una suite completa de pruebas unitarias y de integración robustas.
disable-model-invocation: true
---

# Skill: Maestro de Pruebas Unitarias Django

Este skill inspecciona tu código fuente y escribe pruebas automatizadas robustas utilizando el framework nativo `django.test`.

## 📥 Datos Requeridos
Claude, solicita al usuario:
1. El **nombre de la app** que se va a testear.
2. El **archivo de vistas o lógica** específico que requiere la suite de pruebas.

## 🚀 Pasos de Ejecución

Claude, ejecuta las siguientes acciones de forma autónoma:

### 1. Estructura de `tests.py`
- Abre o crea el archivo `tests.py` dentro de la app indicada.
- Importa `TestCase` de `django.test`, `Client` de `django.test.client` y `reverse` de `django.urls`.
- Importa los modelos y formularios de la aplicación.

### 2. Generación de Casos de Prueba (Test Cases)
- Crea una clase de prueba que herede de `TestCase`.
- Implementa el método `setUp(self)` para inyectar datos de prueba base en la base de datos temporal de Django (ej: crear un producto simulado).
- Escribe métodos descriptivos que comiencen con la palabra `test_` (ej: `test_creacion_producto_exitoso`, `test_vista_retorna_200_ok`).
- Utiliza aserciones estrictas de Django:
  - `self.assertEqual(response.status_code, 200)`
  - `self.assertTemplateUsed(response, 'plantilla.html')`
  - `self.assertContains(response, 'Texto Esperado')`

## 🏁 Resultado Esperado
Muestra el código completo inyectado en `tests.py` y ejecuta en segundo plano el comando de consola `python manage.py test <nombre_app>` para verificar y confirmar que todos los tests pasen en verde.
