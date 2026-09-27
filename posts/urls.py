from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('posts/', views.lista_posts, name='lista_posts'),
    path('acerca/', views.acerca, name='acerca'),
]
