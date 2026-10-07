from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Post


def inicio(request):
    # En el inicio muestro los 3 últimos posts publicados
    ultimos_posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')[:3]
    return render(request, 'posts/inicio.html', {'ultimos_posts': ultimos_posts})


def acerca(request):
    return render(request, 'posts/acerca.html')


# ===== CRUD de posts =====

def lista_posts(request):
    # Read: todos los posts, del más nuevo al más viejo.
    # Se muestran también los borradores y archivados para poder editarlos desde el sitio.
    posts = Post.objects.all().order_by("-fecha_creacion")
    context = {
        "posts": posts
    }
    return render(request, "posts/lista_posts.html", context)


def detalle_post(request, pk):
    # Read: un post solo. Si el id no existe, devuelve un error 404.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/detalle_post.html', {'post': post})


def crear_post(request):
    # Create
    if request.method == 'POST':
        # request.POST trae los textos y request.FILES trae la imagen
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, 'El post se creó correctamente.')
            return redirect('detalle_post', pk=post.pk)
    else:
        form = PostForm()

    context = {
        'form': form,
        'titulo_pagina': 'Nuevo post',
        'texto_boton': 'Crear post',
    }
    return render(request, 'posts/post_form.html', context)


def editar_post(request, pk):
    # Update
    post = get_object_or_404(Post, pk=pk)

    # Guardo la imagen que tenía antes de tocar el formulario,
    # para mostrarla en la página y para borrar el archivo si la cambian.
    imagen_anterior = post.imagen.name
    imagen_actual_url = post.imagen.url if post.imagen else None

    if request.method == 'POST':
        # instance=post hace que se actualice este post en vez de crear uno nuevo
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            # Si subieron otra imagen o la quitaron, borro el archivo viejo de media/posts/
            if imagen_anterior and imagen_anterior != post.imagen.name:
                post.imagen.storage.delete(imagen_anterior)
            messages.success(request, 'Los cambios se guardaron.')
            return redirect('detalle_post', pk=post.pk)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'post': post,
        'imagen_actual_url': imagen_actual_url,
        'titulo_pagina': 'Editar post',
        'texto_boton': 'Guardar cambios',
    }
    return render(request, 'posts/post_form.html', context)


def eliminar_post(request, pk):
    # Delete: con GET muestra la confirmación y recién con POST borra
    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        titulo = post.titulo
        if post.imagen:
            post.imagen.delete(save=False)  # borra también el archivo de la imagen
        post.delete()
        messages.success(request, f'Se eliminó el post "{titulo}".')
        return redirect('lista_posts')

    return render(request, 'posts/post_confirm_delete.html', {'post': post})
