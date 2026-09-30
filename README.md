# Blog Django

Blog web hecho con Django, que voy armando a lo largo del curso.

## Descripción

El proyecto se llama `blog_project` y tiene una app principal, `posts`.

En esta etapa el blog ya se puede recorrer desde el navegador: tiene una página de inicio, una lista de posts y una página "Acerca de". Todas comparten el mismo encabezado, menú y pie gracias a un template base, y los estilos salen de un archivo CSS propio.

Desde esta entrega los posts ya no están escritos a mano: se guardan en una base de datos SQLite con el modelo `Post` y se cargan desde el panel de administración de Django.

## Requisitos

- Python 3.10 o más nuevo
- Git

Django no hace falta instalarlo a mano, se instala con el `requirements.txt`.

## Cómo ejecutarlo

### 1. Clonar el repositorio

```bash
git clone https://github.com/Federicoz21/Blog_django.git
```

### 2. Entrar a la carpeta

```bash
cd Blog_django
```

### 3. Crear el entorno virtual

```bash
python -m venv venv
```

### 4. Activar el entorno virtual

En Windows (PowerShell):

```powershell
.\venv\Scripts\Activate.ps1
```

Si PowerShell no te deja ejecutar el script, corré esto una sola vez y probá de nuevo:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

En Windows (CMD):

```cmd
venv\Scripts\activate
```

En Linux o macOS:

```bash
source venv/bin/activate
```

Cuando está activo, aparece `(venv)` al principio de la línea de la terminal.

### 5. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

Esto crea el archivo `db.sqlite3` con las tablas. La base no se sube a GitHub, así que la primera vez hay que correr este comando.

### 7. Crear el superusuario

```bash
python manage.py createsuperuser
```

Pide nombre de usuario, email y contraseña. Con ese usuario se entra al panel de administración.

### 8. Levantar el servidor

```bash
python manage.py runserver
```

Después abrí http://127.0.0.1:8000/ en el navegador. Tendría que aparecer la página de inicio del blog con los estilos aplicados. Para cortar el servidor, `Ctrl + C`.

## Panel de administración

Con el servidor andando, entrá a http://127.0.0.1:8000/admin/ con el usuario y la contraseña del superusuario.

Para cargar un post: en **Posts** tocá **Agregar**, completá título, contenido, autor y estado, y guardá. La fecha no hace falta ponerla, se guarda sola.

En el sitio solo se ven los posts con estado **Publicado**. Los que están en **Borrador** o **Archivado** quedan solo en el admin.

## Páginas del sitio

| Página    | URL                              | Vista         | Template                   |
|-----------|----------------------------------|---------------|----------------------------|
| Inicio    | http://127.0.0.1:8000/           | `inicio`      | `posts/inicio.html`        |
| Posts     | http://127.0.0.1:8000/posts/     | `lista_posts` | `posts/lista_posts.html`   |
| Acerca de | http://127.0.0.1:8000/acerca/    | `acerca`      | `posts/acerca.html`        |
| Admin     | http://127.0.0.1:8000/admin/     | -             | -                          |

Se puede pasar de una a otra con el menú de arriba. La página en la que estás aparece resaltada.

En **Posts** aparecen todos los publicados, del más nuevo al más viejo, y en **Inicio** los 3 últimos.

## Modelo Post

Está en `posts/models.py` y tiene estos campos:

- `titulo`
- `contenido`
- `autor`
- `fecha_creacion` (con `auto_now_add=True`, se completa sola)
- `estado`: borrador, publicado o archivado (con `choices`)

El `__str__` devuelve el título, así en el admin cada post aparece con su nombre.

La migración que crea la tabla es `posts/migrations/0001_initial.py`. Si se cambia el modelo hay que volver a correr `python manage.py makemigrations` y `python manage.py migrate`.

## Cómo está armado

El recorrido de cada pedido es: **ruta → vista → template → estático**.

1. `blog_project/urls.py` incluye las rutas de la app con `include('posts.urls')`.
2. `posts/urls.py` define un `path` para cada página y le pone nombre (`inicio`, `lista_posts`, `acerca`).
3. La vista `lista_posts` trae los posts publicados con el ORM y los manda al template:
   ```python
   posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
   ```
4. `lista_posts.html` los recorre con `{% for post in posts %}` y muestra el título, el contenido, el autor y la fecha.
5. Los templates hijos arrancan con `{% extends 'posts/base.html' %}` y completan el `{% block content %}`.
6. `base.html` tiene `{% load static %}` al principio y enlaza el CSS con `{% static 'posts/css/estilos.css' %}`.

Los links del menú usan `{% url 'nombre' %}`, así que si algún día cambia una dirección, se toca solo en `urls.py`.

En `posts/admin.py` el modelo está registrado con una clase `PostAdmin` que muestra las columnas título, autor, estado y fecha de creación.

## Estructura

```
Blog_django/
├── manage.py
├── requirements.txt
├── README.md
├── .gitignore
├── blog_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations/
    │   ├── __init__.py
    │   └── 0001_initial.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── templates/
    │   └── posts/
    │       ├── base.html
    │       ├── inicio.html
    │       ├── lista_posts.html
    │       └── acerca.html
    └── static/
        └── posts/
            └── css/
                └── estilos.css
```

Los templates y el CSS van dentro de una carpeta con el nombre de la app (`templates/posts/` y `static/posts/`) para que no se mezclen con los de otras apps si el proyecto crece.

## Configuración

Lo que se cambió en `blog_project/settings.py`:

- La app `posts` está registrada en `INSTALLED_APPS` como `'posts.apps.PostsConfig'`.
- Idioma: `LANGUAGE_CODE = 'es-ar'` (español de Argentina).
- Zona horaria: `TIME_ZONE = 'America/Argentina/Buenos_Aires'`.

El `.gitignore` deja afuera el entorno virtual (`venv/`), los archivos `__pycache__` y `.pyc`, el `.env` y la base local `db.sqlite3`.

## Aplicaciones

- `posts`: app principal del blog. Tiene el modelo `Post`, las vistas, las rutas, los templates y el CSS del sitio.

## Dependencias

Están en `requirements.txt`:

- Django 5.2.17
- asgiref, sqlparse y tzdata (vienen con Django)

Si instalás algo nuevo, acordate de actualizar el archivo con `pip freeze > requirements.txt`. Ojo en Windows: en PowerShell ese comando guarda el archivo en UTF-16 y GitHub no lo puede leer. Conviene hacerlo desde CMD o con:

```powershell
pip freeze | Out-File -Encoding ascii requirements.txt
```

## Entregas

- Preentrega 7 (base del proyecto Django y app `posts`): quedó guardada tal cual se entregó en la rama [`preentrega-7`](https://github.com/Federicoz21/Blog_django/tree/preentrega-7).
- Preentrega 8 (templates, herencia, rutas, vistas y CSS): quedó guardada en la rama [`preentrega-8`](https://github.com/Federicoz21/Blog_django/tree/preentrega-8).
- Preentrega 9 (modelo `Post`, migraciones y panel admin): es lo que está en `main`.

## Autor

Federico Zangaro
