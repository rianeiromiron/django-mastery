"""
ASGI para CI (ver settings_ci.py). asgi.py normal importa siempre
`dashboard.routing`, que no existe en el checkout de CI salvo que la app
bajo prueba sea justamente `dashboard` — por eso ese import queda
condicionado a CI_APP_NAME en vez de ser incondicional.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_mastery.settings_ci')

django_asgi_app = get_asgi_application()

if os.environ.get('CI_APP_NAME') == 'dashboard':
    from channels.auth import AuthMiddlewareStack
    from channels.routing import ProtocolTypeRouter, URLRouter

    from dashboard.routing import websocket_urlpatterns

    application = ProtocolTypeRouter({
        'http': django_asgi_app,
        'websocket': AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    })
else:
    application = django_asgi_app
