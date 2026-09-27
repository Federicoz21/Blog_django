# Blog Django

Base de un blog web hecho con Django.

## Descripción

Este repo tiene el punto de partida del blog: el proyecto `blog_project` ya creado y configurado, y la app `posts`, que es donde después van a ir las publicaciones.

Por ahora no hay modelos, vistas ni templates propios. La idea de esta etapa es dejar la estructura ordenada y funcionando para ir sumando el resto en las próximas entregas.

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

### 6. Levantar el servidor

```bash
python manage.py runserver
```

Después abrí http://127.0.0.1:8000/ en el navegador. Si aparece la pantalla de bienvenida de Django, está todo bien. Para cortar el servidor, `Ctrl + C`.

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
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## Configuración

Lo que se cambió en `blog_project/settings.py`:

- La app `posts` está registrada en `INSTALLED_APPS` como `'posts.apps.PostsConfig'`.
- Idioma: `LANGUAGE_CODE = 'es-ar'` (español de Argentina).
- Zona horaria: `TIME_ZONE = 'America/Argentina/Buenos_Aires'`.

El `.gitignore` deja afuera el entorno virtual (`venv/`), los archivos `__pycache__` y `.pyc`, el `.env` y la base local `db.sqlite3`.

## Aplicaciones

- `posts`: app principal del blog. Acá se van a manejar las publicaciones.

## Dependencias

Están en `requirements.txt`:

- Django 5.2.17
- asgiref, sqlparse y tzdata (vienen con Django)

Si instalás algo nuevo, acordate de actualizar el archivo con `pip freeze > requirements.txt`. Ojo en Windows: en PowerShell ese comando guarda el archivo en UTF-16 y GitHub no lo puede leer. Conviene hacerlo desde CMD o con:

```powershell
pip freeze | Out-File -Encoding ascii requirements.txt
```

## Autor

Federico Zangaro
