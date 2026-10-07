from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Formulario para crear y editar posts, armado a partir del modelo Post."""

    class Meta:
        model = Post
        fields = ['titulo', 'contenido', 'autor', 'estado', 'imagen']
        labels = {
            'titulo': 'Título',
            'contenido': 'Contenido',
            'autor': 'Autor',
            'estado': 'Estado',
            'imagen': 'Imagen (opcional)',
        }
        widgets = {
            'titulo': forms.TextInput(attrs={'placeholder': 'El título del post'}),
            'contenido': forms.Textarea(attrs={'rows': 10, 'placeholder': 'Escribí el post acá...'}),
            'autor': forms.TextInput(attrs={'placeholder': 'Tu nombre'}),
            # accept hace que el navegador muestre solo imágenes al elegir el archivo
            'imagen': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
