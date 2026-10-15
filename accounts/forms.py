from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Perfil


class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=False, label='Correo electrónico')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': 'Nombre de usuario'}


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia', 'link_web', 'avatar']
        labels = {
            'biografia': 'Biografía',
            'link_web': 'Página web (opcional)',
            'avatar': 'Foto de perfil',
        }
        widgets = {
            'biografia': forms.Textarea(attrs={'rows': 5}),
            'avatar': forms.ClearableFileInput(attrs={'accept': 'image/*'}),
        }
