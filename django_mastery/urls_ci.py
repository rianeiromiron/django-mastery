"""
URLconf mínimo para CI (ver settings_ci.py): monta solo las urls de la app
bajo prueba (CI_APP_NAME), en vez de las 9 apps que arma urls.py normal.
"""

import os

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

_CI_APP_NAME = os.environ['CI_APP_NAME']

urlpatterns = [
    path('admin/', admin.site.urls),
    # settings.LOGIN_URL = 'login' - varias apps (ej. tweets) usan
    # @login_required y necesitan poder resolver este nombre aunque la app
    # que normalmente lo registra (membresia) no esté presente en CI.
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('', include(f"{_CI_APP_NAME}.urls")),
]

if _CI_APP_NAME != 'blog_estatico':
    # blog_estatico/base.html (el layout que extienden varias apps) usa
    # {% url 'home' %} / {% url 'about' %} en la nav - hace falta montar
    # sus urls para que resuelvan aunque no sea la app bajo prueba.
    urlpatterns.append(path('_blog_estatico/', include('blog_estatico.urls')))
