"""
Settings usados SOLO por los pipelines de CI de cada app (ver skill
ci-pipeline). Cada app tiene su propio repo y su propio Actions workflow,
que clona este repo (django_mastery) para poder arrancar Django, pero solo
trae consigo la app que se está probando — las otras 8 no existen en ese
checkout. `INSTALLED_APPS`/`ROOT_URLCONF` normales (settings.py/urls.py)
asumen las 9 apps presentes y romperían el arranque.

Estos settings recortan la app instalada a la que indique la variable de
entorno CI_APP_NAME, para que el pipeline de una app no dependa del estado
de las otras 8.
"""

import os

from .settings import *

CI_APP_NAME = os.environ['CI_APP_NAME']

_CORE_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    # blog_estatico no tiene modelos ni se registra en urls_ci: se incluye
    # solo para que su templates/blog_estatico/base.html (el layout base
    # que extienden varias apps) resuelva via APP_DIRS en CI aislado.
    'blog_estatico',
]

INSTALLED_APPS = _CORE_APPS + ([CI_APP_NAME] if CI_APP_NAME not in _CORE_APPS else [])
ROOT_URLCONF = 'django_mastery.urls_ci'
