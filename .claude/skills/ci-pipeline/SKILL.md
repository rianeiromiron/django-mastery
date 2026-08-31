---
name: ci-pipeline
description: Agrega un pipeline de GitHub Actions (lint con ruff, mypy y manage.py test contra Django + Redis + Celery reales via docker-compose) a una de las apps de django_mastery que tiene su propio repositorio git.
disable-model-invocation: true
---

# Skill: Pipeline de CI (lint + test) para apps de django_mastery

Agrega un workflow `lint-and-test` de GitHub Actions a una app que vive en
su propio repositorio (`blog_estatico`, `gestor_tareas`, `catalogo`,
`membresia`, `eventos`, `dashboard`, `libreria`, `tweets`, `tienda` — ver
sección 15/16 de `PROYECTO.md`). Corre `ruff`, `mypy` y los tests reales de
la app contra Django + Redis + Celery levantados con `docker-compose`.

## ⚠️ Contexto importante antes de empezar

- Cada app es su **propio repo git con su propio remoto** dentro de
  `SKILLS/` (el repo raíz `django_mastery`, público en GitHub). Todos los
  comandos de `git` deben ejecutarse con el `cd` puesto en la carpeta de la
  app — **nunca** corras nada de git/ruff/docker desde la raíz de `SKILLS/`
  cuando el cambio es para una app, se tocaría el repo equivocado (ya pasó
  una vez: un `ruff --fix` corrido sin `cd` modificó `django_mastery/asgi.py`
  por accidente).
- Las apps son *apps* de Django, no proyectos standalone: no tienen
  `manage.py`/`settings.py`/`requirements.txt` propios. Para poder correr
  `manage.py test` de verdad, el pipeline de cada app **clona también el
  repo raíz `rianeiromiron/django-mastery`** (es público) y copia el
  código de la app adentro.
- **`settings.py`/`urls.py`/`asgi.py` normales exigen las 9 apps
  presentes** (`INSTALLED_APPS`, `django_mastery/urls.py`, y el import de
  `dashboard.routing` en `asgi.py`) — si el pipeline de una sola app
  intentara usarlos, Django no arrancaría. Por eso existen, ya creados en
  el repo raíz, `django_mastery/settings_ci.py`, `urls_ci.py` y
  `asgi_ci.py`: arman un `INSTALLED_APPS`/URLconf mínimo con solo la app
  que indique la variable de entorno `CI_APP_NAME` (+ las apps base de
  Django). También registran a mano la URL `login` genérica, porque varias
  apps usan `@login_required` (que depende de `settings.LOGIN_URL`) sin
  tener instalada la app `membresia`, que es quien normalmente la define.
  **No dupliques esta lógica por app** — reusa estos archivos tal cual.
- `docker-compose.ci.yml` (raíz) es un *override* de `docker-compose.yml`
  que apunta `web`/`celery_worker` a esos settings de CI, sin tocar el
  compose normal. `mypy.ini` (raíz) trae una config permisiva con
  `django-stubs` apuntando a `settings_ci`.
- Antes de escribir nada en un repo de app, valida en local con el venv
  del proyecto (`.venv/Scripts/python.exe`, o el equivalente en tu
  sistema) que la app arranca aislada:
  ```
  CI_APP_NAME=<app> python manage.py check --settings=django_mastery.settings_ci
  CI_APP_NAME=<app> python manage.py test <app> --settings=django_mastery.settings_ci
  ```
  Si algo falla ahí, decide junto al usuario si es un bug real de la app
  (como pasó con `tweets`, que ya fallaba igual con los settings normales)
  o si hace falta ajustar `settings_ci.py`/`urls_ci.py` (por ejemplo, otra
  dependencia cruzada entre apps tipo la de `login`). No sigas adelante
  con el pipeline hasta que esto pase.

## 📥 Datos requeridos

Pregunta al usuario (si no lo dijo ya) el nombre de la app/carpeta a la que
hay que agregarle el pipeline.

## 🚀 Pasos de ejecución

1. **Verificar el repo:** confirma que `<app>/.git` existe y que tiene un
   remoto (`git -C <app> remote -v`). Si no tiene remoto, avisa y detente.
2. **Validar el aislamiento en local** con los comandos de la sección
   anterior. Resuelve cualquier fallo antes de seguir.
3. **Crear/actualizar el workflow** en
   `<app>/.github/workflows/lint-and-test.yml`:
   ```yaml
   name: lint-and-test

   on:
     push:
     pull_request:

   env:
     CI_APP_NAME: <app>

   jobs:
     lint-and-test:
       runs-on: ubuntu-latest
       steps:
         - name: Checkout code
           uses: actions/checkout@v4
           with:
             path: app

         - name: Checkout django_mastery
           uses: actions/checkout@v4
           with:
             repository: rianeiromiron/django-mastery
             path: django_mastery

         - name: Copiar la app dentro de django_mastery
           run: |
             rm -rf "django_mastery/${CI_APP_NAME}"
             cp -r app "django_mastery/${CI_APP_NAME}"

         - name: Crear .env de prueba
           working-directory: django_mastery
           run: |
             cat > .env <<EOF
             DEBUG=True
             SECRET_KEY=ci-test-secret-key
             ALLOWED_HOSTS=localhost,127.0.0.1
             EMAIL_HOST_USER=ci@example.com
             EMAIL_HOST_PASSWORD=ci-fake-password
             STRIPE_PUBLIC_KEY=pk_test_ci
             STRIPE_SECRET_KEY=sk_test_ci
             STRIPE_WEBHOOK_SECRET=whsec_ci
             CI_APP_NAME=${CI_APP_NAME}
             EOF

         - name: Build and start Django + Redis + Celery
           working-directory: django_mastery
           run: docker compose -f docker-compose.yml -f docker-compose.ci.yml up -d --build

         - name: Wait for Django to be ready
           run: |
             for i in $(seq 1 30); do
               if curl -sf http://localhost:8000/admin/login/ > /dev/null; then
                 echo "Django listo"
                 exit 0
               fi
               sleep 2
             done
             echo "Django nunca respondio"
             exit 1

         - uses: actions/setup-python@v5
           with:
             python-version: "3.13"

         - name: Run Ruff
           working-directory: app
           run: |
             pip install ruff
             ruff check .

         - name: Run mypy
           working-directory: django_mastery
           run: |
             docker compose exec -T web pip install --no-cache-dir mypy django-stubs
             docker compose exec -T web mypy "${CI_APP_NAME}"

         - name: Run tests
           working-directory: django_mastery
           run: docker compose exec -T web python manage.py test "${CI_APP_NAME}"

         - name: Tear down
           if: always()
           working-directory: django_mastery
           run: docker compose -f docker-compose.yml -f docker-compose.ci.yml down -v
   ```
   (Reemplaza `<app>` por el nombre real en `env.CI_APP_NAME` y en el
   nombre del workflow.) Si el repo tenía un `lint.yml` viejo de solo
   ruff, bórralo — este workflow ya incluye ruff.
4. **Crear `<app>/ruff.toml`** si no existe, para ignorar `N999` (se
   dispara porque GitHub Actions clona el repo en una carpeta con guion,
   ej. `django-blog_estatico`, y ruff la confunde con un nombre de módulo
   inválido — no es un error real del código):
   ```toml
   [lint]
   # N999 (nombre de modulo invalido) se dispara por el guion en el nombre
   # del repo, que GitHub Actions usa como carpeta al clonar - no tiene
   # relacion con el codigo de la app.
   ignore = ["N999"]
   ```
5. **Correr ruff localmente antes de subir nada**, con el `cd` puesto en
   la carpeta de la app:
   ```
   cd <ruta absoluta a la app> && ruff check --fix .
   ```
   Revisa el diff de cada archivo que `--fix` haya tocado antes de seguir.
   Si aparece algo que no sea un fix mecánico esperable, muéstraselo al
   usuario y pregunta antes de continuar. Vuelve a correr `ruff check .`
   (sin `--fix`) para confirmar 0 errores.
6. **Revisar qué se va a commitear:** con `git -C <app> status --short`,
   confirma que solo se agregan los archivos de este cambio. Si hay
   cambios previos sin relación en la carpeta, no los incluyas en el
   commit.
7. **Proponer el mensaje de commit** (convención `<tipo>(<alcance>):
   <descripción>`, ver skill `formatear_mensajes_commit`) y pedir
   aprobación antes de aplicarlo.
8. **Push:** confirma con el usuario antes de `git -C <app> push` (es una
   acción visible en GitHub).
9. **Verificar el Action:** con `gh -C <app> run list --limit 3` y
   `gh -C <app> run watch <id> --exit-status`, confirma que el pipeline
   corrió y pasó en verde. Si falla, muestra el log
   (`gh -C <app> run view <id> --log-failed`), explica el error al
   usuario y repite desde el paso correspondiente tras corregirlo. Un
   fallo en "Run tests" puede ser un bug real y preexistente de la app
   (no asumas que es un problema del pipeline) — compáralo corriendo la
   misma prueba en local contra los settings normales del proyecto antes
   de tocar nada.

## 🏁 Resultado esperado

El repo de la app tiene `.github/workflows/lint-and-test.yml` y
`ruff.toml` commiteados y pusheados, y el último Action de GitHub para ese
repo aparece en verde con los pasos: checkout, build de Django+Redis+
Celery, ruff, mypy y tests reales de la app.
