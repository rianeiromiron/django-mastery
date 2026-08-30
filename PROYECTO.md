# PROYECTO.md — Bitácora para reconstrucción

> Este archivo documenta todo el trabajo hecho en este proyecto con Claude Code,
> con el objetivo de poder reconstruirlo desde cero (con otra cuenta, otra
> herramienta, o manualmente) si se pierde el acceso a esta sesión o repositorio.
> Última actualización: 2026-08-28.

## 1. Visión general

Proyecto de aprendizaje de Django llamado **`django_mastery`**, ubicado en
`c:\Code\CLAUDECODEPROJECTS\SKILLS`. Cada "proyecto" de práctica es una app de
Django independiente, con **su propio repositorio git y su propio repo remoto
en GitHub** (no hay un único repo para todo `SKILLS`).

Apps creadas hasta ahora:

| App | Descripción | Repo GitHub |
|-----|-------------|-------------|
| `blog_estatico` | Blog personal estático (posts en memoria) | https://github.com/rianeiromiron/django-blog_estatico |
| `gestor_tareas` | Gestor de tareas con modelo en BD (Proyecto 2) | https://github.com/rianeiromiron/django-gestor_tareas |
| `catalogo` | Catálogo de productos con búsqueda, filtro por categoría, paginación y diseño con tarjetas (Proyecto 3) | https://github.com/rianeiromiron/django-catalogo |
| `membresia` | Sistema de membresía con contenido exclusivo protegido por login (Proyecto 4) | https://github.com/rianeiromiron/django-membresia |
| `libreria` | Catálogo de libros con API REST (Django REST Framework) (Proyecto 5) | https://github.com/rianeiromiron/django-libreria |
| `eventos` | Registro de asistentes a un evento, con confirmación de asistencia reactiva vía HTMX (Proyecto 6) | https://github.com/rianeiromiron/django-eventos |
| `dashboard` | Dashboard en tiempo real (Proyecto 7) con Django Channels: vista + plantilla que muestra una tarjeta de "carga de CPU" actualizada en vivo vía WebSocket, sin recargar la página | https://github.com/rianeiromiron/django-dashboard |
| `tweets` | Muro de tweets (Proyecto 8) con procesamiento asíncrono: publicar tweets y disparar un newsletter en segundo plano vía Celery + Redis, que envía un email real | https://github.com/rianeiromiron/django-tweets |
| `tienda` | Pasarela de pago (Proyecto 9) con Stripe Checkout: modelo `Pedido`, vista que crea una sesión de pago y redirige a Stripe, páginas de éxito/cancelación, y webhook (`checkout.session.completed`) que marca el pedido como `pagado` | https://github.com/rianeiromiron/django-tienda |

Cuenta de GitHub: **rianeiromiron**. El CLI `gh` está instalado y autenticado
en esta máquina (scopes: gist, read:org, repo).

## 2. Estructura de carpetas (raíz `SKILLS`)

```
SKILLS/
├── .env                      # SECRET_KEY, DEBUG (no versionado, ver sección 3)
├── .gitignore                # gitignore general (la raíz NO es un repo git)
├── .venv/                    # entorno virtual del proyecto (ver sección 3)
├── db.sqlite3                # base de datos local (no versionada)
├── manage.py
├── requirements.txt
├── static/
├── django_mastery/           # paquete de configuración del proyecto Django
│   ├── settings.py
│   ├── urls.py                # urls raíz, incluye las de cada app
│   ├── asgi.py                 # ProtocolTypeRouter (HTTP + WebSockets, ver sección 12)
│   ├── wsgi.py
├── blog_estatico/             # app 1 — repo git propio, remoto propio
├── gestor_tareas/              # app 2 — repo git propio, remoto propio
├── catalogo/                   # app 3 — repo git propio, remoto propio
├── membresia/                  # app 4 — repo git propio, remoto propio
├── libreria/                   # app 5 — repo git propio, remoto propio
├── eventos/                     # app 6 — repo git propio, remoto propio
├── dashboard/                    # app 7 — repo git propio, remoto propio
├── tweets/                        # app 8 — repo git propio, remoto propio
├── tienda/                         # app 9 — repo git propio, remoto propio
└── .claude/skills/            # skills locales del proyecto (make-model, init-django,
                                # orm-wizard, auth-audit, gen-api, htmx-ui, channel-guide,
                                # celery-worker, test-master)
```

**Importante:** la carpeta raíz `SKILLS` **no** es un repositorio git. Cada app
que ya se considera "terminada" (`blog_estatico`, `gestor_tareas`, `catalogo`,
`membresia`, `eventos`, `dashboard`, `libreria`, `tweets`, `tienda`) tiene su
propio `.git` interno y su propio remoto en GitHub, creado con
`gh repo create ... --source=<carpeta_app> --remote=origin`.

## 3. Entorno de ejecución

- Python: se usa un entorno virtual **dentro del propio proyecto**:
  `SKILLS/.venv/`. **Ojo:** en esta máquina el comando `python` global apunta a
  otro entorno virtual no relacionado (`C:\Code\python\dia2-django\venv`) que
  no tiene `python-dotenv` instalado y rompe `manage.py`. Por eso, todos los
  comandos de Django deben ejecutarse explícitamente con el intérprete del
  proyecto:
  ```bash
  ./.venv/Scripts/python.exe manage.py <comando>
  ```
- `requirements.txt` (actualizado tras instalar Django REST Framework para
  `libreria`, Django Channels + Daphne para `dashboard`, Celery + Redis para
  `tweets`, y el SDK de Stripe para `tienda`):
  ```
  amqp==5.3.1
  asgiref==3.12.1
  attrs==26.1.0
  autobahn==26.7.1
  Automat==25.4.16
  billiard==4.2.4
  cbor2==6.1.4
  celery==5.6.3
  certifi==2026.7.22
  cffi==2.1.1
  channels==4.3.2
  charset-normalizer==3.5.1
  click==8.5.0
  click-didyoumean==0.3.1
  click-plugins==1.1.1.2
  click-repl==0.3.0
  constantly==23.10.4
  cryptography==50.0.1
  daphne==4.2.3
  Django==6.1
  djangorestframework==3.18.0
  hyperlink==21.0.0
  idna==3.19
  Incremental==24.11.0
  kombu==5.6.2
  msgpack==1.2.2
  packaging==26.3
  prompt_toolkit==3.0.53
  pycparser==3.0
  pyOpenSSL==26.4.0
  python-dateutil==2.9.0.post0
  python-dotenv==1.2.3
  redis==8.1.0
  requests==2.34.2
  service-identity==26.1.0
  six==1.17.0
  sqlparse==0.6.0
  stripe==15.6.0
  Twisted==26.4.0
  txaio==26.6.1
  typing_extensions==4.16.0
  tzdata==2026.3
  tzlocal==5.4.4
  ujson==5.13.0
  urllib3==2.7.0
  vine==5.1.0
  wcwidth==0.8.3
  zope.interface==8.6
  ```
- `.env` (en la raíz, no versionado) define `SECRET_KEY`, `DEBUG`, y —desde
  `tweets` (ver sección 13)— `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD`
  (contraseña de aplicación de Gmail, no la contraseña normal de la cuenta).
  **Nota:** las credenciales de Stripe de `tienda` (sección 14) **no** están en
  `.env` — quedaron como literales directamente en `settings.py`, a pedido
  explícito del usuario en la instrucción original. Como `django_mastery/` no
  pertenece a ningún repo git (la raíz `SKILLS` no es un repo), no se suben a
  ningún remoto, pero si se quisiera reforzar la práctica sería mejor
  moverlas a `.env` igual que `SECRET_KEY`/`EMAIL_HOST_PASSWORD`.
  Se carga en `django_mastery/settings.py` con `python-dotenv`
  (`load_dotenv(BASE_DIR / '.env')`). Para reconstruir: crear un `.env` con:
  ```
  SECRET_KEY=<una clave secreta de Django>
  DEBUG=True
  EMAIL_HOST_USER=<tu email de Gmail>
  EMAIL_HOST_PASSWORD=<contraseña de aplicación de Gmail, 16 caracteres>
  ```
- Base de datos: SQLite (`db.sqlite3`), no versionada.
- **Redis:** corre en un contenedor Docker (`redis:7-alpine`, puerto `6379`)
  compartido con otro proyecto local (`dia2-django-redis-1`); no se creó un
  contenedor dedicado para `django_mastery`. Si no está corriendo:
  `docker start dia2-django-redis-1` (o levantar cualquier Redis en
  `localhost:6379`).

## 4. `django_mastery/settings.py` — puntos clave

```python
INSTALLED_APPS = [
    'daphne',                    # debe ir ANTES que 'channels' (ver nota abajo)
    'channels',                  # debe ir ANTES que las apps nativas de Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog_estatico',
    'gestor_tareas',
    'catalogo',
    'membresia',
    'libreria',
    'rest_framework',
    'eventos',
    'dashboard',
    'tweets',
    'tienda',
]
```

Se agregó, para soportar Channels (ver sección 12):
```python
ASGI_APPLICATION = 'django_mastery.asgi.application'
```
**Importante:** `'daphne'` debe ir **antes** de `'channels'` en `INSTALLED_APPS`. Sin
`'daphne'` ahí, `manage.py runserver` sigue arrancando el servidor WSGI clásico
de Django (no soporta el *upgrade* a WebSocket) en vez del servidor
ASGI/Daphne — el síntoma es `404 Not Found` al conectar a `ws/metricas/`. Este
bug se encontró y corrigió al verificar el dashboard en el navegador (ver
sección 12).

Resto de settings sin cambios respecto al `startproject` por defecto de Django
6.1 (SQLite, `TEMPLATES` con `APP_DIRS=True` y `DIRS=[]`, `STATIC_URL='static/'`, etc),
salvo las siguientes claves agregadas al final del archivo para el sistema de
autenticación de `membresia` (ver sección 9):

```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'panel_exclusivo'
LOGOUT_REDIRECT_URL = 'login'
```

Se agregaron, para soportar Celery + email real en `tweets` (ver sección 13):
```python
# Celery
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Email (SMTP real de Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```
**Nota:** antes de esto existía una clave `MAILERS` (un dict con
`django.core.mail.backends.console.EmailBackend`) que **no es un setting real
de Django** — Django solo lee `EMAIL_BACKEND` (string). Era configuración
muerta; se detectó y se reemplazó al implementar el envío real de correo en
`tweets`.

Se agregaron, para soportar Stripe Checkout + webhooks en `tienda` (ver
sección 14):
```python
# Stripe
STRIPE_PUBLIC_KEY = 'pk_test_...'
STRIPE_SECRET_KEY = 'sk_test_...'
STRIPE_WEBHOOK_SECRET = 'whsec_...'
```
A diferencia del resto de las credenciales del proyecto, estas **no** se
leen desde `.env` — quedaron como literales en `settings.py` a pedido
explícito del usuario (ver nota en sección 3).

## 5. `django_mastery/urls.py` (raíz del proyecto)

```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tareas/', include('gestor_tareas.urls')),
    path('catalogo/', include('catalogo.urls')),
    path('membresia/', include('membresia.urls')),
    path('api/libreria/', include('libreria.urls')),
    path('eventos/', include('eventos.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('tweets/', include('tweets.urls')),
    path('tienda/', include('tienda.urls')),
    path('', include('blog_estatico.urls')),
]
```
(el prefijo `tweets/` se agregó, junto con `dashboard/`, antes del catch-all
de `blog_estatico`, igual que el resto de las apps — ver sección 13; `tienda/`
se agregó de la misma forma — ver sección 14).

## 6. App `blog_estatico`

Blog personal con posts de ejemplo definidos **en memoria** (sin modelo de BD).
Repo git propio con remoto `origin` → `https://github.com/rianeiromiron/django-blog_estatico.git`.
Historial: commit único `feat(blog): agrega vistas, plantillas y rutas`.

### `blog_estatico/views.py`
```python
from django.http import Http404
from django.shortcuts import render

POSTS = [
    {
        "id": 1,
        "title": "Bienvenido a mi blog",
        "excerpt": "Un primer vistazo a lo que planeo compartir aquí.",
        "date": "2026-01-10",
        "body": "Este es el primer post de mi blog personal. Aquí iré compartiendo "
                "notas sobre desarrollo web, Python y Django.",
    },
    {
        "id": 2,
        "title": "Aprendiendo Django",
        "excerpt": "Mis notas mientras exploro el framework Django.",
        "date": "2026-02-05",
        "body": "Django ofrece una estructura clara para construir aplicaciones web: "
                "modelos, vistas, plantillas y un sistema de rutas muy flexible.",
    },
    {
        "id": 3,
        "title": "Plantillas y herencia en Django",
        "excerpt": "Cómo reutilizar HTML con {% block %} y {% extends %}.",
        "date": "2026-03-02",
        "body": "El sistema de plantillas de Django permite definir una base común "
                "y extenderla en cada página, evitando repetir código HTML.",
    },
]


def home(request):
    return render(request, "blog_estatico/home.html", {"posts": POSTS})


def post_detail(request, post_id):
    post = next((p for p in POSTS if p["id"] == post_id), None)
    if post is None:
        raise Http404("Post no encontrado")
    return render(request, "blog_estatico/post_detail.html", {"post": post})


def about(request):
    return render(request, "blog_estatico/about.html")
```

### `blog_estatico/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("about/", views.about, name="about"),
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),
]
```

### `blog_estatico/models.py` / `admin.py`
Sin modelo definido (`# Create your models here.` / `# Register your models here.` sin uso).

### Plantillas (`blog_estatico/templates/blog_estatico/`)

`base.html` — plantilla base global del proyecto (la usan también otras apps,
p. ej. `gestor_tareas`, `catalogo`, `membresia` y `eventos`, vía
`{% extends "blog_estatico/base.html" %}`, gracias a que `APP_DIRS=True` busca
en las carpetas `templates/` de todas las apps). Incluye un bloque opcional
`{% block extra_head %}{% endblock %}` antes de `</head>` para que otras apps
puedan inyectar `<link rel="stylesheet">` propios sin tocar este archivo
compartido (usado por `catalogo`, ver sección 8). Además, en la etapa de
`eventos` (ver sección 11) se agregaron aquí, globalmente, los CDN de
**Tailwind CSS** y **HTMX**:
```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Blog Personal{% endblock %}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/htmx.org@1.9.12"></script>
    {% block extra_head %}{% endblock %}
</head>
<body>
    <header>
        <h1><a href="{% url 'home' %}">Mi Blog Personal</a></h1>
        <nav>
            <a href="{% url 'home' %}">Inicio</a>
            <a href="{% url 'about' %}">Sobre mí</a>
        </nav>
    </header>

    <main>
        {% block content %}{% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 Mi Blog Personal</p>
    </footer>
</body>
</html>
```

`home.html`:
```html
{% extends "blog_estatico/base.html" %}
{% block title %}Inicio - Blog Personal{% endblock %}
{% block content %}
    <h2>Últimos posts</h2>
    <ul>
        {% for post in posts %}
        <li>
            <a href="{% url 'post_detail' post.id %}">{{ post.title }}</a>
            <p>{{ post.excerpt }}</p>
        </li>
        {% endfor %}
    </ul>
{% endblock %}
```

`post_detail.html`:
```html
{% extends "blog_estatico/base.html" %}
{% block title %}{{ post.title }} - Blog Personal{% endblock %}
{% block content %}
    <article>
        <h2>{{ post.title }}</h2>
        <p><em>{{ post.date }}</em></p>
        <p>{{ post.body }}</p>
    </article>
{% endblock %}
```

`about.html`:
```html
{% extends "blog_estatico/base.html" %}
{% block title %}Sobre mí - Blog Personal{% endblock %}
{% block content %}
    <h2>Sobre el autor</h2>
    <p>
        Hola, soy el autor de este blog. Escribo sobre desarrollo web,
        Python y las cosas que voy aprendiendo en el camino.
    </p>
{% endblock %}
```

## 7. App `gestor_tareas` (Proyecto 2)

Gestor de tareas con modelo persistido en BD. Creada con
`python manage.py startapp gestor_tareas` y registrada en `INSTALLED_APPS`.
Repo git propio con remoto `origin` → `https://github.com/rianeiromiron/django-gestor_tareas.git`.
Historial:
1. `feat(gestor_tareas): app inicial de gestor de tareas`
2. `docs(gestor_tareas): traduce el readme al ingles`

### `gestor_tareas/models.py`
```python
from django.db import models


class Tarea(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    completado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
```

### `gestor_tareas/forms.py`
```python
from django import forms
from .models import Tarea


class TareaForm(forms.ModelForm):
    class Meta:
        model = Tarea
        fields = ['titulo', 'descripcion']
```

### `gestor_tareas/views.py`
```python
from django.shortcuts import redirect, render
from .forms import TareaForm
from .models import Tarea


def lista_tareas(request):
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_tareas')
    else:
        form = TareaForm()

    tareas = Tarea.objects.all().order_by('-fecha_creacion')
    return render(request, 'gestor_tareas/lista.html', {'form': form, 'tareas': tareas})
```

### `gestor_tareas/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_tareas, name='lista_tareas'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `tareas/` (ver sección 5).

### `gestor_tareas/admin.py`
```python
from django.contrib import admin
from .models import Tarea


@admin.register(Tarea)
class TareaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'completado', 'fecha_creacion')
```

### `gestor_tareas/templates/gestor_tareas/lista.html`
```html
{% extends "blog_estatico/base.html" %}

{% block title %}Gestor de Tareas{% endblock %}

{% block content %}
    <h2>Nueva tarea</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Guardar tarea</button>
    </form>

    <h2>Tareas</h2>
    <ul>
        {% for tarea in tareas %}
        <li>
            <strong>{{ tarea.titulo }}</strong>
            {% if tarea.completado %}
                ✅ Completada
            {% else %}
                ⏳ Pendiente
            {% endif %}
            {% if tarea.descripcion %}
                <p>{{ tarea.descripcion }}</p>
            {% endif %}
        </li>
        {% empty %}
        <li>No hay tareas todavía.</li>
        {% endfor %}
    </ul>
{% endblock %}
```

### Migraciones
`gestor_tareas/migrations/0001_initial.py` crea el modelo `Tarea` tal como se
define arriba. Se generó con:
```bash
./.venv/Scripts/python.exe manage.py makemigrations gestor_tareas
./.venv/Scripts/python.exe manage.py migrate gestor_tareas
```

### `gestor_tareas/README.md`
En inglés (traducido desde una primera versión en español). Describe el
modelo, formulario, vista, plantilla, ruta y admin — mismo contenido que las
secciones de arriba, en formato README para GitHub.

## 8. App `catalogo` (Proyecto 3)

Catálogo de productos con modelo persistido en BD, búsqueda de texto, filtro
por categoría, paginación y una interfaz visual con tarjetas (creada con el
skill `orm-wizard` para la lógica de consultas, y luego "embellecida" a
pedido). Creada con `python manage.py startapp catalogo` y registrada en
`INSTALLED_APPS`. Repo git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-catalogo.git`.
Historial:
1. `feat(catalogo): app inicial de catalogo de productos`
2. `feat(catalogo): rediseña la pagina del catalogo con tarjetas y estilos`

### `catalogo/models.py`
```python
from django.db import models


class Producto(models.Model):
    CATEGORIA_CHOICES = [
        ('electronica', 'Electrónica'),
        ('ropa', 'Ropa'),
        ('hogar', 'Hogar'),
    ]

    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=20, choices=CATEGORIA_CHOICES)
    fecha_ingreso = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nombre
```

### `catalogo/views.py`
Búsqueda por texto (`q`, con `Q(nombre__icontains=...) | Q(descripcion__icontains=...)`),
filtro exacto por categoría (`categoria`) y paginación con `Paginator` (2
productos por página, a propósito, para poder probar Anterior/Siguiente con
pocos datos):
```python
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Producto


def lista_productos(request):
    productos = Producto.objects.all()

    query = request.GET.get('q', '')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(descripcion__icontains=query)
        )

    categoria = request.GET.get('categoria', '')
    if categoria:
        productos = productos.filter(categoria=categoria)

    paginator = Paginator(productos, 2)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'page_obj': page_obj,
        'productos': page_obj.object_list,
        'query': query,
        'categoria_seleccionada': categoria,
        'categorias': Producto.CATEGORIA_CHOICES,
    }
    return render(request, 'catalogo/lista_productos.html', context)
```

### `catalogo/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `catalogo/` (ver sección 5).

### `catalogo/admin.py`
```python
from django.contrib import admin

from .models import Producto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'categoria', 'precio', 'fecha_ingreso')
```

### Plantillas y estilos
- `catalogo/templates/catalogo/lista_productos.html` — extiende
  `blog_estatico/base.html`; formulario de búsqueda/filtro (`q`, `categoria`),
  grid de tarjetas (una por producto, con badge de categoría vía
  `get_categoria_display`), estado vacío y paginación Anterior/Siguiente que
  preserva los filtros activos.
- `catalogo/static/catalogo/css/style.css` — hoja de estilos propia de la app
  (cargada desde `lista_productos.html` vía el bloque `extra_head` de
  `base.html`): hero con gradiente, tarjetas con `hover`, badges de color por
  categoría (Electrónica=azul, Ropa=rosa, Hogar=verde), paginación tipo
  píldora.

### Migraciones
```bash
./.venv/Scripts/python.exe manage.py makemigrations catalogo
./.venv/Scripts/python.exe manage.py migrate catalogo
```

### `catalogo/README.md`
En inglés. Describe modelo, vistas (búsqueda/filtro/paginación), plantilla,
rutas y admin.

## 9. App `membresia` (Proyecto 4)

Sistema de membresía con contenido exclusivo protegido por login, usando las
vistas de autenticación nativas de Django (`django.contrib.auth.views`).
Creada con `python manage.py startapp membresia` y registrada en
`INSTALLED_APPS`. Repo git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-membresia.git`.

### `membresia/models.py`
```python
from django.db import models


class ContenidoExclusivo(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.TextField()
    nivel = models.CharField(max_length=50)

    def __str__(self):
        return self.titulo
```
`nivel` es un `CharField` libre (sin `choices`), con valores de ejemplo
Bronce/Plata/Oro, a diferencia de `categoria` en `catalogo` que sí usa
`choices`.

### `membresia/views.py`
```python
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import ContenidoExclusivo


@login_required
def panel_exclusivo(request):
    contenidos = ContenidoExclusivo.objects.all()
    return render(request, 'membresia/panel.html', {'contenidos': contenidos})
```
`panel_exclusivo` se creó **a propósito sin** `@login_required` primero, para
poder probar el skill `auth-audit` (ver sección 15) y que lo detectara y
corrigiera — el decorador de arriba es el resultado de esa auditoría.

### `membresia/urls.py`
```python
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('panel/', views.panel_exclusivo, name='panel_exclusivo'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `membresia/` (ver sección 5).
`login`/`logout` usan las vistas nativas de Django (`LoginView`/`LogoutView`)
sin `template_name` explícito, porque `LoginView` busca por defecto
`registration/login.html`.

### `membresia/admin.py`
```python
from django.contrib import admin

from .models import ContenidoExclusivo


@admin.register(ContenidoExclusivo)
class ContenidoExclusivoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'nivel')
```

### Plantillas
- `membresia/templates/registration/login.html` — ruta específica donde
  `LoginView` busca la plantilla por defecto. Extiende `blog_estatico/base.html`;
  formulario `POST` simple con `{{ form.as_p }}` y `{% csrf_token %}`.
- `membresia/templates/membresia/panel.html` — extiende `blog_estatico/base.html`;
  itera `contenidos` con `{% for %}` (sin botones sensibles, por lo que no
  aplica el chequeo de `{% if user.is_authenticated %}` en plantillas).

### Configuración de autenticación (`django_mastery/settings.py`)
```python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'panel_exclusivo'
LOGOUT_REDIRECT_URL = 'login'
```
`LOGIN_URL` se agregó durante la auditoría de `auth-audit` (no estaba definida
globalmente; sin ella, `@login_required` habría redirigido al valor por
defecto de Django `/accounts/login/`, ruta inexistente en este proyecto, en
vez de a `/membresia/login/`).

### Migraciones
```bash
./.venv/Scripts/python.exe manage.py makemigrations membresia
./.venv/Scripts/python.exe manage.py migrate membresia
```

## 10. App `libreria` (Proyecto 5)

Catálogo de libros expuesto tanto por el admin de Django como por una **API
REST** construida con Django REST Framework (`djangorestframework` agregado a
`INSTALLED_APPS` y a `requirements.txt`). Tiene repo git local propio
(`libreria/.git`, un commit: `feat(libreria): agrega modelo libro y api rest`)
pero **todavía no tiene remoto en GitHub** — falta el paso `gh repo create`.

### `libreria/models.py`
```python
from django.db import models


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=200)
    sinopsis = models.TextField()
    paginas = models.IntegerField()

    def __str__(self):
        return self.titulo
```

### `libreria/serializers.py`
```python
from rest_framework import serializers

from .models import Libro


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'
```

### `libreria/views.py`
```python
from rest_framework import viewsets

from .models import Libro
from .serializers import LibroSerializer


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer
```

### `libreria/urls.py`
CRUD completo vía `DefaultRouter`:
```python
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LibroViewSet

router = DefaultRouter()
router.register(r'libros', LibroViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `api/libreria/` (ver
sección 5). Endpoints: `GET/POST /api/libreria/libros/` y
`GET/PUT/PATCH/DELETE /api/libreria/libros/{id}/`.

### `libreria/admin.py`
```python
from django.contrib import admin

from .models import Libro


@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'paginas')
```

### `libreria/README.md`
En inglés. Documenta el modelo, el admin, los endpoints de la API REST (con
ejemplo de respuesta JSON) y cómo instalarla de forma standalone.

### Migraciones
```bash
./.venv/Scripts/python.exe manage.py makemigrations libreria
./.venv/Scripts/python.exe manage.py migrate libreria
```

Repo git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-libreria.git`.

## 11. App `eventos` (Proyecto 6)

Registro de asistentes a un evento con confirmación de asistencia **reactiva**
(sin recargar la página), usando HTMX + Tailwind CSS. Creada con
`python manage.py startapp eventos` y registrada en `INSTALLED_APPS`. Repo git
propio con remoto `origin` → `https://github.com/rianeiromiron/django-eventos.git`.
Historial: commit único `feat(eventos): app de registro con htmx`.

### `eventos/models.py`
```python
from django.db import models


class Asistente(models.Model):
    nombre = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    confirmado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre
```
Generado con el skill `make-model` (ver sección 15).

### `eventos/admin.py`
```python
from django.contrib import admin

from .models import Asistente


@admin.register(Asistente)
class AsistenteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'email', 'confirmado')
```

### `eventos/views.py`
Generado con el skill `htmx-ui` (ver sección 15). `registro_evento` (GET)
renderiza la página completa; `confirmar_asistencia` (POST, llamada por HTMX)
solo actualiza el campo `confirmado` y devuelve el fragmento del botón:
```python
from django.shortcuts import get_object_or_404, render

from .models import Asistente


def registro_evento(request):
    asistentes = Asistente.objects.all()
    return render(request, 'eventos/registro.html', {'asistentes': asistentes})


def confirmar_asistencia(request, pk):
    asistente = get_object_or_404(Asistente, pk=pk)
    if request.method == 'POST':
        asistente.confirmado = True
        asistente.save()
    return render(request, 'eventos/fragmento_boton.html', {'asistente': asistente})
```

### `eventos/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.registro_evento, name='registro_evento'),
    path('confirmar/<int:pk>/', views.confirmar_asistencia, name='confirmar_asistencia'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `eventos/` (ver sección 5).
Página principal: **`http://127.0.0.1:8000/eventos/`**.

### Plantillas (`eventos/templates/eventos/`)
- `registro.html` — extiende `blog_estatico/base.html`; tarjeta con Tailwind
  que lista los asistentes (nombre, email) e incluye, por cada uno, el
  fragmento del botón de confirmación.
- `fragmento_boton.html` — fragmento intercambiable por HTMX: si el asistente
  no está confirmado, muestra un botón `hx-post` hacia `confirmar_asistencia`
  con `hx-target`/`hx-swap="outerHTML"`; si ya está confirmado, muestra un
  badge verde en su lugar.

### CDNs globales
Los `<script>` de Tailwind CSS y HTMX se agregaron en el `<head>` de
`blog_estatico/templates/blog_estatico/base.html` (compartido por todas las
apps, ver sección 6):
```html
<script src="https://cdn.tailwindcss.com"></script>
<script src="https://unpkg.com/htmx.org@1.9.12"></script>
```

### Migraciones
```bash
./.venv/Scripts/python.exe manage.py makemigrations eventos
./.venv/Scripts/python.exe manage.py migrate eventos
```

### `eventos/README.md`
En inglés. Documenta el modelo, las vistas, las plantillas, las rutas y el
admin.

## 12. App `dashboard` (Proyecto 7)

Dashboard en tiempo real con Django Channels (WebSockets). Creada con
`python manage.py startapp dashboard` y registrada en `INSTALLED_APPS`. Repo
git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-dashboard.git`.
Historial: commit único `feat(dashboard): agrega dashboard con websockets`.
No tiene modelo de BD (la app es puramente sobre la capa ASGI/WebSocket).

### Dependencias
Se instaló `channels[daphne]` (`channels==4.3.2`, `daphne==4.2.3`, y su árbol
de dependencias: `autobahn`, `twisted`, `cryptography`, etc. — ver
`requirements.txt` en la sección 3).

### `django_mastery/settings.py`
```python
INSTALLED_APPS = [
    'channels',   # AL PRINCIPIO, antes de las apps nativas de Django
    ...
    'dashboard',
]

ASGI_APPLICATION = 'django_mastery.asgi.application'
```

### `django_mastery/asgi.py`
Convertido en un enrutador de protocolos (`ProtocolTypeRouter`) que separa
tráfico HTTP normal de tráfico WebSocket, delegando este último al
`URLRouter` de `dashboard.routing`, envuelto en `AuthMiddlewareStack` (para
tener `scope['user']` disponible en los consumers):
```python
import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_mastery.settings')

django_asgi_app = get_asgi_application()

from dashboard.routing import websocket_urlpatterns  # noqa: E402

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(websocket_urlpatterns)
    ),
})
```

### `dashboard/routing.py`
```python
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/metricas/$', consumers.MetricasConsumer.as_asgi()),
]
```

### `dashboard/consumers.py`
`MetricasConsumer` implementado como **`AsyncWebsocketConsumer`** (variante
asíncrona, recomendada para trabajar con Daphne). `connect()` acepta la
conexión y lanza una tarea de fondo (`asyncio.create_task`) que emite un valor
aleatorio de CPU (20-80) cada 2-3 segundos vía `self.send(...)`;
`disconnect()` cancela esa tarea para no dejarla corriendo indefinidamente
tras cerrar la conexión:
```python
import asyncio
import json
import random

from channels.generic.websocket import AsyncWebsocketConsumer


class MetricasConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.tarea_metricas = asyncio.create_task(self.emitir_metricas())

    async def disconnect(self, close_code):
        self.tarea_metricas.cancel()

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def emitir_metricas(self):
        while True:
            cpu = random.randint(20, 80)
            await self.send(text_data=json.dumps({'cpu': cpu}))
            await asyncio.sleep(random.uniform(2, 3))
```

### `dashboard/views.py` y `dashboard/urls.py`
```python
from django.shortcuts import render


def ver_dashboard(request):
    return render(request, 'dashboard/index.html')
```
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.ver_dashboard, name='ver_dashboard'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `dashboard/` (ver sección
5). Página principal: **`http://127.0.0.1:8000/dashboard/`**.

### Plantilla (`dashboard/templates/dashboard/index.html`)
Extiende `blog_estatico/base.html` (Tailwind cargado globalmente ahí). Tarjeta
con `<span id="cpu-valor">` y `<p id="ws-estado">`; un `<script>` abre
`new WebSocket('ws://' + window.location.host + '/ws/metricas/')` y en
`socket.onmessage` hace `JSON.parse(e.data)` y actualiza `cpu-valor` con
`datos.cpu`. `socket.onopen`/`onclose` actualizan el texto de `ws-estado`
("Conectado"/"Desconectado").

### Bug encontrado y corregido: falta `'daphne'` en `INSTALLED_APPS`
Al verificar el dashboard en el navegador (con Playwright/Chromium headless),
la conexión WebSocket fallaba con `404 Not Found` en `/ws/metricas/`. Causa:
solo `'channels'` estaba en `INSTALLED_APPS`, pero **`manage.py runserver`
solo usa el servidor ASGI/Daphne si `'daphne'` está registrado como app**
(antes de `'channels'`); sin eso, sigue usando el servidor WSGI clásico, que
no soporta el *upgrade* a WebSocket. Se agregó `'daphne'` al inicio de
`INSTALLED_APPS` (ver sección 4). Tras el fix, el log de `runserver` muestra
`Starting ASGI/Daphne version 4.2.3 development server` en vez de
`Starting WSGI development server`.

### Verificación
- `python manage.py check` corrido sin errores.
- Verificación end-to-end en navegador (Playwright, Chromium headless):
  `ws-estado` pasa a "Conectado", `cpu-valor` cambia varias veces sin recargar
  la página (valores observados en una corrida: 49 → 36 → 28), sin errores de
  consola. El log del servidor confirma el ciclo completo:
  `WebSocket HANDSHAKING` → `CONNECT` → `DISCONNECT`.

### `dashboard/README.md`
En inglés. Documenta la arquitectura (routing, consumer, vista, plantilla),
las rutas, el requisito de `'daphne'` en `INSTALLED_APPS` y cómo correr la
app.

### Pendiente
- Reemplazar el valor simulado de CPU por métricas reales.
- Si en el futuro varios clientes deben compartir el mismo feed en vivo
  (broadcast), configurar `CHANNEL_LAYERS` (no está definido todavía) y usar
  grupos de canal (`group_send`) en vez de `self.send` directo.

## 13. App `tweets` (Proyecto 8)

Muro de tweets con procesamiento asíncrono: publicar tweets (persistidos en
BD) y disparar, desde un botón aparte, un newsletter que se procesa en
segundo plano vía **Celery + Redis** y termina enviando un **correo real**.
Creada con `python manage.py startapp tweets` y registrada en
`INSTALLED_APPS`. Repo git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-tweets.git`.
Historial: commit único `feat(tweets): agrega app de tweets con newsletter via celery`.

### Motor de Celery a nivel de proyecto

No existía Celery en el proyecto antes de `tweets`; se agregó la
infraestructura completa:

`django_mastery/celery.py`:
```python
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_mastery.settings')

app = Celery('django_mastery')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

`django_mastery/__init__.py`:
```python
from .celery import app as celery_app

__all__ = ('celery_app',)
```
(hace que `@shared_task` se registre al arrancar Django). Configuración de
broker/backend y del SMTP de email en `settings.py`, ver sección 4.

### `tweets/models.py`
```python
from django.db import models


class Tweet(models.Model):
    usuario = models.CharField(max_length=150)
    contenido = models.CharField(max_length=280)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    contenido2 = models.CharField(max_length=280)

    def __str__(self):
        return f"{self.usuario}: {self.contenido[:50]}"
```
Generado con el skill `make-model` (ver sección 15). `usuario` no tiene
`choices` ni relación a `auth.User` — es un `CharField` libre "para
simplificar", a pedido explícito del usuario.

`contenido2` se agregó después, a pedido del usuario, sin un propósito
funcional específico todavía (no está expuesto en `TweetForm` ni en la
plantilla del muro — ver secciones siguientes). Requirió su propia migración,
ver "Migraciones" más abajo.

### `tweets/forms.py`
`TweetForm` (`ModelForm`) expone **solo** el campo `contenido`, con un
widget `Textarea` estilizado con Tailwind (`maxlength=280`, placeholder
"¿Qué está pasando?"). `usuario` queda fuera del formulario a propósito.

### `tweets/views.py`
```python
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import TweetForm
from .models import Tweet
from .tasks import enviar_newsletter_async


def muro_tweets(request):
    if request.method == 'POST':
        form = TweetForm(request.POST)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.usuario = request.user.username if request.user.is_authenticated else 'Anónimo'
            tweet.save()
            return redirect('muro_tweets')
    else:
        form = TweetForm()

    tweets = Tweet.objects.all().order_by('-fecha_publicacion')
    return render(request, 'tweets/muro.html', {'form': form, 'tweets': tweets})


def enviar_newsletter(request):
    if request.method == 'POST':
        asunto = 'Novedades de Tweets'
        mensaje = 'Estas son las novedades de esta semana en la comunidad de Tweets.'
        destinatarios = ['ana@example.com', 'bruno@example.com']

        enviar_newsletter_async.delay(asunto, mensaje, destinatarios)

        messages.info(request, 'El envío del newsletter se inició en segundo plano con Celery.')

    return redirect('muro_tweets')
```
Como el form no incluye `usuario`, la vista lo completa con
`request.user.username` si hay sesión iniciada, o `'Anónimo'` si no (la app
`tweets` no tiene su propio sistema de login). `destinatarios` empezó
hardcodeado con el email personal real del usuario (para probar el envío a
su propia bandeja); antes de subir el repo a GitHub (público) se reemplazó
por emails ficticios (`ana@example.com`, `bruno@example.com`) para no
exponer un email real en el código fuente público — ver sección "Auditoría y
correcciones" más abajo.

### `tweets/tasks.py`
```python
import time

from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def enviar_newsletter_async(self, asunto, mensaje, destinatarios):
    try:
        time.sleep(5)
        send_mail(
            subject=asunto,
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=destinatarios,
        )
        return f"Newsletter '{asunto}' enviada correctamente a {len(destinatarios)} destinatarios."
    except Exception as exc:
        raise self.retry(exc=exc)
```
`time.sleep(5)` simula el costo de un envío masivo. El envío real de correo
se agregó **después** de una primera versión que solo simulaba el envío (sin
`send_mail`), a pedido del usuario, que quería ver un correo real llegar a su
bandeja.

### `tweets/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.muro_tweets, name='muro_tweets'),
    path('enviar-newsletter/', views.enviar_newsletter, name='enviar_newsletter'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `tweets/` (ver sección
5). Página principal: **`http://127.0.0.1:8000/tweets/`**.

### `tweets/admin.py`
```python
from django.contrib import admin

from .models import Tweet


@admin.register(Tweet)
class TweetAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'contenido', 'fecha_publicacion', 'contenido2')
```

### Plantilla (`tweets/templates/tweets/muro.html`)
Extiende `blog_estatico/base.html` (Tailwind cargado globalmente ahí).
Arriba: tarjeta con mensajes de Django (`{% if messages %}`), el formulario
de composición (`Textarea` + botón "Twittear") y, al lado del encabezado, un
botón morado "🚀 Enviar Newsletter (Celery)" que hace `POST` a
`enviar_newsletter`. Abajo: feed de tarjetas con usuario, contenido y fecha
(`|date:"d M Y, H:i"`), con estado vacío si no hay tweets todavía.

### `tweets/tests.py`
5 tests (`manage.py test tweets` → `OK`):
- `MuroTweetsViewTests`: POST crea un `Tweet` y redirige (302); GET lista los
  tweets en orden `-fecha_publicacion`.
- `EnviarNewsletterViewTests`: POST invoca `enviar_newsletter_async.delay`
  (mockeado, sin necesitar Redis/worker real); GET no dispara la tarea.
- `EnviarNewsletterTaskTests`: llama la tarea **directamente** (no vía
  `.delay()`, sin necesitar broker), mockeando `time.sleep` para no esperar
  los 5s reales, y verifica el correo capturado en `django.core.mail.outbox`
  (Django reemplaza `EMAIL_BACKEND` por `locmem` automáticamente en tests).

### Migraciones
```bash
./.venv/Scripts/python.exe manage.py makemigrations tweets
./.venv/Scripts/python.exe manage.py migrate tweets
```
- `0001_initial.py` — modelo `Tweet` original (`usuario`, `contenido`,
  `fecha_publicacion`).
- `0002_tweet_contenido2.py` — agrega el campo `contenido2`. Causó un
  `OperationalError: no such column: tweets_tweet.contenido2` en el admin
  hasta que se generó y aplicó esta migración (el modelo se había editado
  sin correr `makemigrations`/`migrate`).

### `tweets/README.md`
En inglés. Documenta el modelo, las vistas, la tarea de Celery, la plantilla,
los tests y las rutas.

### Cómo correr Celery localmente (Windows)
```bash
./.venv/Scripts/python.exe -m celery -A django_mastery worker --loglevel=info --pool=solo
```
`--pool=solo` es necesario en Windows (el pool `prefork` por defecto no
funciona bien ahí). Requiere Redis corriendo en `localhost:6379` (ver
sección 3) y `runserver` activo en otra terminal.

### Auditoría con el skill `celery-worker` y correcciones aplicadas
Se ejecutó el skill `celery-worker` (ver sección 15) sobre todo el proyecto
después de armar la integración. Hallazgos:
- Entorno del proyecto (`celery.py`, autocarga de tareas, `CELERY_BROKER_URL`
  en `settings.py`): sin fallos.
- `tweets/tasks.py`: **fallo detectado** — `enviar_newsletter_async` hacía
  una operación externa (envío de correo) sin reintentos automáticos ante
  fallos de red. Se corrigió agregando
  `bind=True, max_retries=3, default_retry_delay=60` y el bloque
  `try/except` con `self.retry(exc=exc)` (ya reflejado en el código de arriba).

Aparte de la auditoría del skill, durante la implementación se encontraron y
corrigieron dos problemas más:
1. **`MAILERS` no es un setting real de Django** (ver sección 4) — se
   reemplazó por `EMAIL_BACKEND` real.
2. **Un token de acceso personal de GitHub (`ghp_...`) se pegó por error** en
   `EMAIL_HOST_PASSWORD` del `.env` (dos veces, la segunda vez solo se le
   había quitado el prefijo `ghp_`) en vez de la contraseña de aplicación de
   Gmail. Se detectó por el formato (36 caracteres vs. los 16 típicos de una
   contraseña de aplicación) y se le indicó al usuario revocar ese token en
   GitHub y generar la credencial correcta en
   `myaccount.google.com/apppasswords`.

### Verificación end-to-end realizada
Con Redis (contenedor Docker), el worker de Celery y `runserver` corriendo,
se disparó un POST real a `/tweets/enviar-newsletter/` (simulando el botón
del muro). El worker procesó la tarea en ~7s y el log confirmó éxito:
```
Task tweets.tasks.enviar_newsletter_async[...] succeeded in 7.1s:
'Newsletter 'Novedades de Tweets' enviada correctamente a 2 destinatarios.'
```
El usuario confirmó haber recibido el correo real en su bandeja de Gmail.
Al terminar la prueba, se detuvieron el worker y `runserver` (el contenedor
de Redis se dejó corriendo, es compartido con otro proyecto).

### Pendiente
- Los destinatarios del newsletter (`ana@example.com`, `bruno@example.com`)
  siguen hardcodeados en la vista — no hay un formulario ni modelo de
  suscriptores todavía.
- No hay límite de longitud aplicado en el modelo para `usuario` más allá de
  `max_length=150` (elegido arbitrariamente, sin relación a un sistema de
  autenticación real).

## 14. App `tienda` (Proyecto 9)

Pasarela de pago con **Stripe Checkout**: un modelo `Pedido`, una vista que
crea una sesión de pago hospedada por Stripe y redirige al cliente, páginas
de éxito/cancelación, y un webhook que marca el pedido como pagado cuando
Stripe confirma el cobro. Creada con `python manage.py startapp tienda` y
registrada en `INSTALLED_APPS`. Repo git propio con remoto `origin` →
`https://github.com/rianeiromiron/django-tienda.git`.
Historial: `feat(tienda): checkout de pago con stripe` (commit inicial).

### `tienda/models.py`
```python
from django.db import models


class Pedido(models.Model):
    cliente = models.CharField(max_length=255)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_checkout_id = models.CharField(max_length=255, blank=True)
    pagado = models.BooleanField(default=False)
    fecha_pedido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pedido #{self.pk} - {self.cliente}"
```
Generado con el skill `make-model` (ver sección 15).

### `tienda/admin.py`
```python
from django.contrib import admin

from .models import Pedido


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'monto', 'pagado', 'fecha_pedido')
```

### `tienda/views.py`
```python
from decimal import Decimal

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import Pedido

stripe.api_key = settings.STRIPE_SECRET_KEY

PRODUCTO_NOMBRE = 'Suscripción Premium Curso Django'
PRODUCTO_MONTO = Decimal('29.99')


def crear_sesion_pago(request):
    if request.method == 'POST':
        pedido = Pedido.objects.create(
            cliente=request.user.username if request.user.is_authenticated else 'Invitado',
            monto=PRODUCTO_MONTO,
            pagado=False,
        )

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': PRODUCTO_NOMBRE,
                    },
                    'unit_amount': int(pedido.monto * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('pago_exitoso')),
            cancel_url=request.build_absolute_uri(reverse('pago_cancelado')),
            client_reference_id=str(pedido.pk),
        )

        pedido.stripe_checkout_id = checkout_session.id
        pedido.save()

        return redirect(checkout_session.url, permanent=False)

    return render(request, 'tienda/checkout.html', {
        'producto_nombre': PRODUCTO_NOMBRE,
        'producto_monto': PRODUCTO_MONTO,
    })


def pago_exitoso(request):
    return render(request, 'tienda/exito.html')


def pago_cancelado(request):
    return render(request, 'tienda/cancelado.html')


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.error.SignatureVerificationError):
        return HttpResponse(status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        pedido_id = session['client_reference_id']
        if pedido_id:
            Pedido.objects.filter(pk=pedido_id).update(pagado=True)

    return HttpResponse(status=200)
```
El monto y el nombre del producto están hardcodeados (`PRODUCTO_NOMBRE`,
`PRODUCTO_MONTO`) — no hay todavía un catálogo de productos ni un carrito;
es un único "producto" de ejemplo. `client_reference_id` es la clave que
conecta la sesión de Stripe con el `Pedido` local: se manda al crear la
sesión y se vuelve a leer en el webhook para saber qué pedido marcar como
pagado.

### `tienda/urls.py`
```python
from django.urls import path

from . import views

urlpatterns = [
    path('', views.crear_sesion_pago, name='crear_sesion_pago'),
    path('exito/', views.pago_exitoso, name='pago_exitoso'),
    path('cancelado/', views.pago_cancelado, name='pago_cancelado'),
    path('webhook/', views.stripe_webhook, name='stripe_webhook'),
]
```
Incluida en `django_mastery/urls.py` bajo el prefijo `tienda/` (ver sección
5). Página principal: **`http://127.0.0.1:8000/tienda/`**.

### Plantillas (`tienda/templates/tienda/`)
- `checkout.html` — extiende `blog_estatico/base.html` (Tailwind cargado
  globalmente ahí). Tarjeta centrada con el resumen del producto, el monto, y
  un formulario `POST` a `crear_sesion_pago` con el botón "🔒 Proceder al
  Pago seguro con Stripe".
- `exito.html` — confirmación simple de pago exitoso.
- `cancelado.html` — mensaje de cancelación con un link para volver a
  intentar el pago.

### `tienda/tests.py`
7 tests (`manage.py test tienda` → `OK`), generados con el skill
`test-master` (ver sección 15):
- `PedidoModelTest`: el pedido se crea en BD con los datos correctos y en
  estado `pagado=False` por defecto.
- `CrearSesionPagoViewTest`: GET devuelve `200` y usa `checkout.html`; POST
  crea el `Pedido`, redirige (`302`) a la URL de Stripe y guarda el
  `stripe_checkout_id` (con `stripe.checkout.Session.create` mockeado, sin
  llamar a la API real).
- `StripeWebhookViewTest`: un evento `checkout.session.completed` válido
  marca el `Pedido` correspondiente como pagado; una firma inválida devuelve
  `400` y no lo modifica (con `stripe.Webhook.construct_event` mockeado).

### `tienda/README.md`
En inglés. Documenta el modelo, las vistas (incluido el webhook), la
configuración de Stripe (llaves + cómo probar el webhook local con el
Stripe CLI), las plantillas, los tests y las rutas.

### Configuración de Stripe y verificación end-to-end

1. Se instaló el SDK (`pip install stripe`) y se agregaron `STRIPE_PUBLIC_KEY`
   / `STRIPE_SECRET_KEY` a `settings.py` con valores de placeholder
   (`pk_test_ejemplo123` / `sk_test_ejemplo123`) para poder correr
   `manage.py check` sin necesitar una cuenta de Stripe todavía.
2. El usuario creó una cuenta de Stripe y reemplazó las llaves por las reales
   de modo test/sandbox. En el primer intento pegó **la misma cadena** como
   sufijo de ambas llaves (`pk_test_<X>` y `sk_test_<X>` con el mismo `<X>`)
   — se detectó porque en Stripe las llaves pública y secreta nunca comparten
   sufijo, y se le pidió volver a copiarlas del Dashboard
   (`Developers → API keys`).
3. Con las llaves corregidas, la compra de prueba (tarjeta `4242 4242 4242
   4242`) funcionó: la sesión de Stripe Checkout se creó y redirigió
   correctamente, y el `Pedido` quedó guardado con su `stripe_checkout_id`.
   En ese punto `pagado` seguía en `False` a propósito — todavía no había
   webhook.
4. **Implementación del webhook** (a pedido del usuario, para que `pagado`
   se reflejara automáticamente): se agregó `stripe_webhook` (arriba),
   `STRIPE_WEBHOOK_SECRET` en `settings.py`, y la ruta `webhook/`.
5. **Prueba local con Stripe CLI** — problemas encontrados y resueltos:
   - El CLI, tras `stripe login`, quedó autenticado solo contra el contexto
     **`live`** de la cuenta (no la sandbox). `stripe listen --forward-to
     localhost:8000/tienda/webhook/` fallaba pidiendo `--live` o cambiar de
     contexto, y correrlo con `--live` hacía que escuchara eventos de modo
     live — que nunca iban a llegar, porque el checkout se hizo con llaves
     `pk_test_`/`sk_test_` (modo sandbox). Los streams de eventos test y live
     de Stripe son completamente independientes.
   - Solución: volver a correr `stripe login`, y en la página del navegador
     elegir explícitamente el **sandbox** (no `live`) antes de autorizar el
     acceso del CLI. Con eso, `stripe switch context` mostró una segunda fila
     con modo sandbox, y `stripe listen --forward-to
     localhost:8000/tienda/webhook/` (sin `--live`) devolvió un
     `whsec_...` nuevo, específico de la sandbox.
   - El usuario pegó ese secreto sin la `w` inicial (`hsec_...` en vez de
     `whsec_...`) — se detectó por el prefijo y se le pidió volver a
     copiarlo.
   - Con el `whsec_...` correcto, el primer webhook real devolvió `500`. El
     traceback mostró: `AttributeError: 'get' is a dict method, but a
     Session is not a dict. Use .to_dict() to convert it.` — la causa era
     `session.get('client_reference_id')` en `stripe_webhook`:
     `event['data']['object']` en `stripe-python` 15.6.0 no es un `dict`
     plano sino un objeto `Session` tipado, que no implementa `.get()`.
     Se corrigió cambiando a acceso por índice, `session['client_reference_id']`
     (que sí funciona tanto en el objeto real de Stripe como en los `dict`
     usados en los tests). Con la corrección, la compra de prueba siguiente
     marcó el `Pedido` como `pagado=True` correctamente.
6. Cómo repetir la prueba localmente:
   ```bash
   # Terminal 1
   python manage.py runserver
   # Terminal 2 — asegurarse de estar en el contexto sandbox, no live
   stripe switch context
   stripe listen --forward-to localhost:8000/tienda/webhook/
   ```
   Copiar el `whsec_...` impreso a `STRIPE_WEBHOOK_SECRET` en `settings.py`,
   abrir `http://127.0.0.1:8000/tienda/`, pagar con la tarjeta de prueba
   `4242 4242 4242 4242` y verificar `Pedido.objects.get(pk=...).pagado`.

### Pendiente
- No hay catálogo de productos ni carrito — el producto y el monto están
  hardcodeados en `views.py`.
- Las llaves de Stripe están como literales en `settings.py` en vez de
  cargarse desde `.env` (ver nota en sección 3).
- No se probó el flujo de cancelación (`4000 0000 0000 0002` u otra tarjeta
  de rechazo) end-to-end, solo el camino feliz.

## 15. Skills de Claude Code involucrados

### Skills locales del proyecto (`SKILLS/.claude/skills/`)
- **`make-model`** — genera un modelo Django en una app (models.py + admin.py
  con `@admin.register` y `list_display`) y corre `makemigrations` + `migrate`.
  Usado para `Tarea` (`gestor_tareas`), `Producto` (`catalogo`),
  `ContenidoExclusivo` (`membresia`), `Asistente` (`eventos`) y `Pedido`
  (`tienda`). Si la app destino no existe todavía, Claude la crea primero
  con `startapp` y la registra en `INSTALLED_APPS` antes de aplicar el skill
  (así se hizo con `eventos` y `tienda`).
- **`test-master`** — inspecciona `views.py`/`models.py` de una app y escribe
  una suite de tests con `django.test.TestCase`, corriendo
  `manage.py test <app>` al final para confirmar que quedan en verde. Usado
  para `tienda/tests.py` (modelo `Pedido` y las vistas `crear_sesion_pago` /
  `stripe_webhook`, mockeando las llamadas reales a la API de Stripe con
  `unittest.mock.patch`).
- **`init-django`** — automatiza la creación/config inicial de un proyecto Django
  (no se usó en esta sesión para crear `django_mastery`, ya existía).
- **`orm-wizard`** — audita el rendimiento y la lógica de consultas de un
  `views.py` (anti N+1 con `select_related`/`prefetch_related`, búsquedas con
  `Q` objects, paginación robusta con `Paginator`). Usado para agregar
  búsqueda por texto, filtro por categoría y paginación a
  `catalogo/views.py`.
- **`auth-audit`** — inspecciona `views.py`/`urls.py` buscando vistas privadas
  sin `@login_required` (o `LoginRequiredMixin`) ni chequeos
  `{% if user.is_authenticated %}` en plantillas, y corrige lo que encuentra.
  Usado en `membresia/views.py`: detectó `panel_exclusivo` sin protección y
  agregó el decorador + `LOGIN_URL` en `settings.py`.
- **`htmx-ui`** — transforma vistas tradicionales de Django en componentes
  interactivos con HTMX + Tailwind CSS: inyecta los CDNs en `base.html`, crea
  vistas de respuesta parcial (fragmentos HTML) y configura los atributos
  `hx-get`/`hx-post`/`hx-target`/`hx-swap`. Usado para `eventos`
  (`registro_evento` + `confirmar_asistencia`). Nota: el skill trae como
  ejemplo URLs de CDN incompletas (`https://tailwindcss.com`,
  `https://unpkg.com`); Claude las corrigió a las URLs reales
  (`https://cdn.tailwindcss.com`, `https://unpkg.com/htmx.org@1.9.12`).
- **`celery-worker`** (`disable-model-invocation: true`, hay que invocarlo
  explícitamente con `/celery-worker`) — audita el entorno de Celery de un
  proyecto (`celery.py`, autocarga de tareas, `CELERY_BROKER_URL` apuntando a
  Redis) y el `tasks.py` de una app: exige `@shared_task` en las funciones
  costosas y reintentos automáticos (`bind=True, max_retries=3,
  default_retry_delay=60`) si la tarea hace peticiones externas. **Solo
  audita/corrige, no crea modelos ni scaffolding** — la primera vez que se
  invocó por error se le pidió crear el modelo `Tweet` (tarea de
  `make-model`); al confundirse el usuario entre ambos skills, se volvió a
  ejecutar correctamente con `make-model`. Ya con `tweets` construida, se usó
  `celery-worker` para auditar el proyecto completo y detectó que
  `enviar_newsletter_async` no tenía reintentos configurados — Claude lo
  corrigió (ver sección 13).

### Skills globales del usuario (`C:\Users\riane\.claude\skills\`)
- **`generar_readme_github`** — antes de subir un proyecto a GitHub, verifica si
  existe `README.md` en la carpeta destino (detectando ambigüedad si hay
  varias apps/proyectos en la raíz); si no existe, **pregunta al usuario en qué
  idioma generarlo (español o inglés)**, propone contenido basado en el código
  real, y solo lo crea tras aprobación explícita del usuario (SI/NO). Usado
  para `gestor_tareas` (inglés, traducido después), `catalogo` (inglés),
  `membresia` (inglés), `eventos` (inglés), `tweets` (inglés) y `tienda`
  (inglés, actualizado luego para documentar el webhook).
- **`formatear_mensajes_commit`** — genera mensajes de commit con formato
  `<tipo>(<alcance>): <descripción corta en minúsculas>` (tipos: feat, fix,
  docs, test; máx. 50 caracteres primera línea), pide aprobación antes de
  aplicar el commit, y si no hay remoto configurado, ofrece crear el repo en
  GitHub con `gh repo create rianeiromiron/<nombre> --public|--private
  --source=. --remote=origin` (confirmando nombre y visibilidad antes de
  crear) y luego pregunta si hacer `git push`. Usado para publicar
  `gestor_tareas`, `catalogo` (repo `django-catalogo`), `membresia` (repo
  `django-membresia`), `eventos` (repo `django-eventos`), `tweets` (repo
  `django-tweets`, en inglés) y `tienda` (repo `django-tienda`, público). En
  `tienda`, el paso de `gh repo create` fue bloqueado una vez por el
  clasificador de modo automático de Claude Code (acción visible
  externamente); se le explicó al usuario qué se iba a crear y se pidió
  confirmación explícita antes de reintentar.

### Infraestructura sin skill dedicado
La configuración de Django Channels para `dashboard` (sección 12) se hizo
**sin** un skill específico (no existe todavía un skill tipo
`channels-setup`/`websocket-scaffold` en este proyecto); se siguieron las
instrucciones del usuario paso a paso directamente.

## 16. Flujo típico seguido para cada app nueva

1. `startapp` + registrar en `INSTALLED_APPS` + enlazar `urls.py`.
2. Skill `make-model` para generar modelo + admin + migraciones.
3. Vistas, formulario, plantillas y rutas específicas de la app.
   - Si la app necesita búsqueda/filtro/paginación: skill `orm-wizard` sobre
     `views.py` (usado en `catalogo`).
   - Si la app tiene vistas privadas/autenticación: skill `auth-audit` sobre
     `views.py`/`urls.py` para verificar (y corregir) el control de acceso
     (usado en `membresia`).
   - Si la app expone una API REST: agregar `rest_framework`, `serializers.py`
     y un `ModelViewSet` + `DefaultRouter` (usado en `libreria`, sin skill
     dedicado).
   - Si la app necesita interactividad sin recargar la página: skill
     `htmx-ui` sobre `views.py`/plantillas (usado en `eventos`).
   - Si la app necesita procesar algo en segundo plano (envíos masivos,
     tareas lentas): armar `tasks.py` con `@shared_task` manualmente (sin
     skill dedicado para el scaffolding, usado en `tweets`), y después
     auditarlo con el skill `celery-worker` (`/celery-worker`, exige
     reintentos automáticos si la tarea hace peticiones externas).
   - Si la app cobra pagos: integrar el SDK de Stripe manualmente (sin skill
     dedicado para el scaffolding, usado en `tienda`) — crear la sesión de
     Checkout, las páginas de éxito/cancelación, y el webhook
     (`checkout.session.completed`) para reflejar el estado de pago;
     verificar el webhook en local con el Stripe CLI en contexto **sandbox**
     (no `live`).
4. `python manage.py check` para verificar que no hay errores.
5. Skill `test-master` → analiza `views.py`/`models.py`, escribe
   `tests.py` con `django.test.TestCase`, corre `manage.py test <app>` y
   confirma que todo pase en verde (usado en `tienda`).
6. Skill `generar_readme_github` → pregunta carpeta destino, idioma, propone
   contenido, pide aprobación, crea `README.md`.
7. `git init` en la carpeta de la app + `.gitignore` (`__pycache__/`, `*.pyc`)
   + `git add -A`.
8. Skill `formatear_mensajes_commit` → propone mensaje de commit, pide
   aprobación, hace `git commit`.
9. Si no hay remoto: `gh repo create rianeiromiron/<nombre-repo> --public
   --source=. --remote=origin` (nombre y visibilidad confirmados con el
   usuario) y `git push -u origin master`.

## 17. Cómo reconstruir desde cero

1. Crear proyecto Django `django_mastery` (`django-admin startproject django_mastery .`),
   con `python-dotenv` y `.env` como en la sección 3.
2. Instalar dependencias: `pip install -r requirements.txt` (incluye Django,
   `djangorestframework`, `channels[daphne]` con todo su árbol, y
   `celery`/`redis`).
3. Recrear cada app copiando el código de las secciones 6 a 14 tal cual, o
   clonando directamente los repos ya publicados (los que tienen remoto):
   ```bash
   git clone https://github.com/rianeiromiron/django-blog_estatico.git blog_estatico
   git clone https://github.com/rianeiromiron/django-gestor_tareas.git gestor_tareas
   git clone https://github.com/rianeiromiron/django-catalogo.git catalogo
   git clone https://github.com/rianeiromiron/django-membresia.git membresia
   git clone https://github.com/rianeiromiron/django-eventos.git eventos
   git clone https://github.com/rianeiromiron/django-dashboard.git dashboard
   git clone https://github.com/rianeiromiron/django-libreria.git libreria
   git clone https://github.com/rianeiromiron/django-tweets.git tweets
   git clone https://github.com/rianeiromiron/django-tienda.git tienda
   ```
4. Ajustar `INSTALLED_APPS` (incluyendo `'channels'` al principio) y
   `urls.py` raíz como en las secciones 4 y 5, `ASGI_APPLICATION` +
   `django_mastery/asgi.py` como en la sección 12, `django_mastery/celery.py`
   + `django_mastery/__init__.py` + settings de Celery/email como en la
   sección 13, y `STRIPE_PUBLIC_KEY`/`STRIPE_SECRET_KEY`/`STRIPE_WEBHOOK_SECRET`
   (con llaves reales de una cuenta de Stripe, sandbox/test) como en la
   sección 14.
5. `makemigrations` + `migrate` para cada app con modelo (`gestor_tareas`,
   `catalogo`, `membresia`, `libreria`, `eventos`, `tweets`, `tienda`;
   `dashboard` todavía no tiene modelos).
6. Levantar Redis en `localhost:6379` (ver sección 3) y completar
   `EMAIL_HOST_USER`/`EMAIL_HOST_PASSWORD` en `.env` con una contraseña de
   aplicación de Gmail si se quiere que `tweets` envíe correos reales.
7. Para probar el webhook de `tienda` en local: instalar el
   [Stripe CLI](https://docs.stripe.com/stripe-cli), `stripe login`
   autorizando el contexto **sandbox** (no `live`), y
   `stripe listen --forward-to localhost:8000/tienda/webhook/` — copiar el
   `whsec_...` que imprime a `STRIPE_WEBHOOK_SECRET` (ver sección 14).
8. Si se quiere recuperar el comportamiento de los skills personalizados,
   recrear los archivos `SKILL.md` descritos en la sección 15 (o pedirle a
   Claude que los regenere a partir de las descripciones de esta sección).
