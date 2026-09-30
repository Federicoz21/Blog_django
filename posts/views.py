from django.shortcuts import render

from .models import Post


def inicio(request):
    # En el inicio muestro los 3 últimos posts publicados
    ultimos_posts = Post.objects.filter(estado='publicado').order_by('-fecha_creacion')[:3]
    return render(request, 'posts/inicio.html', {'ultimos_posts': ultimos_posts})


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    posts = Post.objects.filter(estado="publicado").order_by("-fecha_creacion")
    context = {
        "posts": posts
    }
    return render(request, "posts/lista_posts.html", context)
