# Blog Django

Blog web hecho con Django, que voy armando a lo largo del curso.

## Descripción

El proyecto se llama `blog_project` y tiene una app principal, `posts`.

El blog se recorre desde el navegador: tiene una página de inicio, una lista de posts y una página "Acerca de". Todas comparten el mismo encabezado, menú y pie gracias a un template base, y los estilos salen de un archivo CSS propio.

Los posts se guardan en una base de datos SQLite con el modelo `Post`.

Desde esta entrega los posts se pueden **crear, ver, editar y eliminar desde el propio sitio** (CRUD), sin pasar por el panel de administración. Además, cada post puede tener una **imagen** que se sube desde el formulario.

## Requisitos

- Python 3.10 o más nuevo
- Git

Django y Pillow no hace falta instalarlos a mano, se instalan con el `requirements.txt`.

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

Esto instala Django y también **Pillow**, que hace falta para las imágenes.

### 6. Aplicar las migraciones

```bash
python manage.py migrate
```

Esto crea el archivo `db.sqlite3` con las tablas. La base no se sube a GitHub, así que la primera vez hay que correr este comando.

Si ya tenías la base de la entrega anterior, este mismo comando le agrega la columna `imagen` a la tabla de posts (migración `0002_post_imagen`). Los posts que ya estaban se conservan y quedan sin imagen.

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

## CRUD de posts

Todas las operaciones se hacen desde el sitio, con vistas basadas en funciones:

| Operación | Qué hace                                   | URL                                          | Vista           | Template                         |
|-----------|--------------------------------------------|----------------------------------------------|-----------------|----------------------------------|
| Listar    | Muestra todos los posts                    | http://127.0.0.1:8000/posts/                 | `lista_posts`   | `posts/lista_posts.html`         |
| Ver       | Muestra un post completo con su imagen     | http://127.0.0.1:8000/posts/1/               | `detalle_post`  | `posts/detalle_post.html`        |
| Crear     | Formulario para un post nuevo              | http://127.0.0.1:8000/posts/crear/           | `crear_post`    | `posts/post_form.html`           |
| Editar    | El mismo formulario, con los datos cargados | http://127.0.0.1:8000/posts/1/editar/        | `editar_post`   | `posts/post_form.html`           |
| Eliminar  | Pide confirmación y después borra          | http://127.0.0.1:8000/posts/1/eliminar/      | `eliminar_post` | `posts/post_confirm_delete.html` |

El `1` es el id del post. Si se pide un id que no existe, la página devuelve un error 404 (con `get_object_or_404`).

Cómo funciona cada una:

- **Listar:** trae todos los posts del más nuevo al más viejo. Cada uno muestra su estado (publicado, borrador o archivado), una miniatura si tiene imagen y los links para verlo, editarlo o eliminarlo.
- **Ver:** muestra título, contenido, autor, estado, fecha e imagen. Si el post no tiene imagen, aparece el aviso "Este post no tiene imagen." y la página no se rompe.
- **Crear:** el formulario es `PostForm`. Si los datos están bien, guarda el post y redirige a su detalle. Si falta algo, vuelve a mostrar el formulario con los errores.
- **Editar:** usa el mismo `PostForm` con `instance=post`, así actualiza ese post en vez de crear otro. Se puede cambiar la imagen o quitarla. Al guardar redirige al detalle.
- **Eliminar:** entrar a la URL solo muestra la página de confirmación (pedido GET). El post se borra recién cuando se aprieta "Sí, eliminar", que manda un pedido POST. Después redirige a la lista.

Después de crear, editar o eliminar aparece un aviso arriba de la página (con el framework de mensajes de Django) para confirmar que salió bien.

En el menú se agregó **Nuevo post**, que lleva directo al formulario de creación.

## Manejo de imágenes

### 1. Campo en el modelo

En `posts/models.py` el modelo `Post` tiene un campo nuevo:

```python
imagen = models.ImageField(upload_to='posts/', null=True, blank=True)
```

- `upload_to='posts/'`: las imágenes se guardan en la carpeta `media/posts/`.
- `null=True` y `blank=True`: la imagen es opcional, un post puede no tener.

### 2. Pillow

`ImageField` necesita la librería **Pillow** para trabajar con imágenes (por ejemplo, para comprobar que lo que se sube es realmente una imagen). Se instaló con:

```bash
pip install Pillow
pip freeze > requirements.txt
```

### 3. Configuración de media en `settings.py`

```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

- `MEDIA_ROOT` es la carpeta del disco donde se guardan los archivos que suben los usuarios.
- `MEDIA_URL` es la dirección desde la que se ven en el navegador. Por ejemplo, una imagen guardada en `media/posts/foto.jpg` se ve en http://127.0.0.1:8000/media/posts/foto.jpg.

### 4. Servir las imágenes en desarrollo (`blog_project/urls.py`)

```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

Con esto, mientras se trabaja con `runserver`, Django sirve los archivos de `media/`. Sin esta línea la imagen se guarda igual, pero en el navegador aparece rota. Va dentro del `if settings.DEBUG` porque en producción eso lo tiene que hacer el servidor web, no Django.

### 5. El formulario (`posts/forms.py`)

`PostForm` hereda de `forms.ModelForm` y está basado en el modelo `Post`, con los campos `titulo`, `contenido`, `autor`, `estado` e `imagen`. Como sale del modelo, no hay que volver a escribir los campos a mano.

En `post_form.html` la etiqueta del formulario tiene:

```html
<form method="post" enctype="multipart/form-data">
```

El `enctype="multipart/form-data"` es obligatorio: sin él, el navegador manda solo los textos y la imagen llega vacía.

### 6. Las vistas reciben `request.FILES`

En `crear_post` y `editar_post` el formulario se arma con los textos **y** con los archivos:

```python
form = PostForm(request.POST, request.FILES)                 # crear
form = PostForm(request.POST, request.FILES, instance=post)  # editar
```

`request.POST` trae los textos y `request.FILES` trae la imagen. Si falta `request.FILES`, la imagen no se guarda.

### 7. Mostrar la imagen en los templates

Antes de usar la URL de la imagen hay que fijarse que el post tenga una, porque si no Django tira error:

```django
{% if post.imagen %}
    <img src="{{ post.imagen.url }}" alt="{{ post.titulo }}">
{% else %}
    <p>Este post no tiene imagen.</p>
{% endif %}
```

La imagen se ve completa en el detalle, como miniatura en la lista y chiquita en la página de confirmación de borrado.

### 8. Para que no queden archivos sueltos

- Al **editar** y subir otra imagen (o quitarla), la vista borra el archivo viejo de `media/posts/`.
- Al **eliminar** un post, también se borra el archivo de su imagen.

### 9. `media/` en GitHub

Las imágenes que se suben no van al repositorio (igual que la base de datos). En el `.gitignore` está:

```
media/posts/*
!media/posts/.gitkeep
```

Así se sube solo la carpeta vacía `media/posts/` (con un archivo `.gitkeep` adentro, porque Git no guarda carpetas vacías) y no las fotos de prueba.

## Cómo probar la carga de imágenes

Con el servidor andando:

1. Entrá a **Nuevo post** (http://127.0.0.1:8000/posts/crear/), completá los datos, elegí una imagen de tu compu y tocá **Crear post**. Te lleva al detalle, donde tiene que verse la imagen.
2. Creá otro post sin elegir imagen. En el detalle aparece "Este post no tiene imagen." en vez de la foto.
3. Entrá a **Posts**: el que tiene imagen muestra la miniatura.
4. En el detalle del primero tocá **Editar**. Arriba del campo de imagen se ve la actual. En **Modificar** elegí otra imagen y guardá: en el detalle aparece la nueva. Para quitarla, marcá la casilla **Eliminar** que está al lado de "Actualmente" y guardá.
5. Tocá **Eliminar** en cualquier post: aparece la confirmación. Con **Cancelar** volvés sin borrar nada; con **Sí, eliminar** se borra y vuelve a la lista.
6. Para ver que la imagen se guardó en el disco, fijate en la carpeta `media/posts/` del proyecto.

También hay tests automáticos que prueban todo el CRUD con imágenes reales (crear con y sin imagen, cambiarla, quitarla, borrar con confirmación, archivos que no son imágenes, etc.):

```bash
python manage.py test posts
```

Los tests guardan las imágenes en una carpeta temporal, así que no ensucian `media/`.

## Panel de administración

Con el servidor andando, entrá a http://127.0.0.1:8000/admin/ con el usuario y la contraseña del superusuario.

Los posts se siguen pudiendo cargar desde ahí también: en **Posts** tocá **Agregar**, completá título, contenido, autor, estado y, si querés, la imagen, y guardá. La fecha no hace falta ponerla, se guarda sola.

## Páginas del sitio

| Página     | URL                                | Vista         | Template                 |
|------------|------------------------------------|---------------|--------------------------|
| Inicio     | http://127.0.0.1:8000/             | `inicio`      | `posts/inicio.html`      |
| Posts      | http://127.0.0.1:8000/posts/       | `lista_posts` | `posts/lista_posts.html` |
| Nuevo post | http://127.0.0.1:8000/posts/crear/ | `crear_post`  | `posts/post_form.html`   |
| Acerca de  | http://127.0.0.1:8000/acerca/      | `acerca`      | `posts/acerca.html`      |
| Admin      | http://127.0.0.1:8000/admin/       | -             | -                        |

Se puede pasar de una a otra con el menú de arriba. La página en la que estás aparece resaltada.

En **Inicio** aparecen los 3 últimos posts **publicados**. En **Posts** aparecen todos, también los borradores y archivados, para poder editarlos desde el sitio. Cuando en el próximo módulo se sumen usuarios y permisos, la idea es que esa gestión quede solo para quien tenga permiso.

## Modelo Post

Está en `posts/models.py` y tiene estos campos:

- `titulo`
- `contenido`
- `autor`
- `fecha_creacion` (con `auto_now_add=True`, se completa sola)
- `estado`: borrador, publicado o archivado (con `choices`)
- `imagen`: opcional, se guarda en `media/posts/`

El `__str__` devuelve el título, así en el admin cada post aparece con su nombre.

Migraciones:

- `posts/migrations/0001_initial.py`: crea la tabla.
- `posts/migrations/0002_post_imagen.py`: agrega el campo `imagen`.

Si se cambia el modelo hay que volver a correr `python manage.py makemigrations` y `python manage.py migrate`.

## Cómo está armado

El recorrido de cada pedido es: **ruta → vista → template → estático**.

1. `blog_project/urls.py` incluye las rutas de la app con `include('posts.urls')` y, en desarrollo, sirve los archivos de `media/`.
2. `posts/urls.py` define un `path` para cada página y le pone nombre (`inicio`, `lista_posts`, `detalle_post`, `crear_post`, `editar_post`, `eliminar_post`, `acerca`). Las del CRUD reciben el id del post con `<int:pk>`.
3. Las vistas de `posts/views.py` usan el ORM para traer, guardar o borrar posts, y `PostForm` para los formularios.
4. Los templates hijos arrancan con `{% extends 'posts/base.html' %}` y completan el `{% block content %}`.
5. `base.html` tiene `{% load static %}` al principio, enlaza el CSS con `{% static 'posts/css/estilos.css' %}` y muestra los avisos de los mensajes.

Los links usan `{% url 'nombre' %}` (y `{% url 'detalle_post' post.pk %}` para los de un post), así que si algún día cambia una dirección, se toca solo en `urls.py`.

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
├── media/
│   └── posts/              ← acá se guardan las imágenes subidas
└── posts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── forms.py
    ├── migrations/
    │   ├── __init__.py
    │   ├── 0001_initial.py
    │   └── 0002_post_imagen.py
    ├── models.py
    ├── tests.py
    ├── urls.py
    ├── views.py
    ├── templates/
    │   └── posts/
    │       ├── base.html
    │       ├── inicio.html
    │       ├── lista_posts.html
    │       ├── detalle_post.html
    │       ├── post_form.html
    │       ├── post_confirm_delete.html
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
- Archivos subidos: `MEDIA_URL = '/media/'` y `MEDIA_ROOT = BASE_DIR / 'media'`.

El `.gitignore` deja afuera el entorno virtual (`venv/`), los archivos `__pycache__` y `.pyc`, el `.env`, la base local `db.sqlite3` y las imágenes subidas a `media/posts/`.

## Aplicaciones

- `posts`: app principal del blog. Tiene el modelo `Post`, el formulario `PostForm`, las vistas del CRUD, las rutas, los templates y el CSS del sitio.

## Dependencias

Están en `requirements.txt`:

- Django 5.2.17
- Pillow 12.3.0 (nueva en esta entrega, para el `ImageField`)
- asgiref, sqlparse y tzdata (vienen con Django)

Si instalás algo nuevo, acordate de actualizar el archivo con `pip freeze > requirements.txt`. Ojo en Windows: en PowerShell ese comando guarda el archivo en UTF-16 y GitHub no lo puede leer. Conviene hacerlo desde CMD o con:

```powershell
pip freeze | Out-File -Encoding ascii requirements.txt
```

## Entregas

- Preentrega 7 (base del proyecto Django y app `posts`): quedó guardada tal cual se entregó en la rama [`preentrega-7`](https://github.com/Federicoz21/Blog_django/tree/preentrega-7).
- Preentrega 8 (templates, herencia, rutas, vistas y CSS): quedó guardada en la rama [`preentrega-8`](https://github.com/Federicoz21/Blog_django/tree/preentrega-8).
- Preentrega 9 (modelo `Post`, migraciones y panel admin): quedó guardada en la rama [`preentrega-9`](https://github.com/Federicoz21/Blog_django/tree/preentrega-9).
- Preentrega 10 (CRUD de posts con imágenes): es lo que está en `main`.

## Autor

Federico Zangaro
