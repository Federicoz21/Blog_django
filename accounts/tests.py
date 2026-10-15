from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Perfil


class UsuariosTests(TestCase):
    def test_registro_crea_perfil(self):
        respuesta = self.client.post(reverse('registro'), {
            'username': 'nuevo',
            'email': 'nuevo@ejemplo.com',
            'password1': 'EjemploCurso2026!',
            'password2': 'EjemploCurso2026!',
        })
        self.assertRedirects(respuesta, reverse('login'))
        usuario = get_user_model().objects.get(username='nuevo')
        self.assertTrue(Perfil.objects.filter(user=usuario).exists())

    def test_perfil_requiere_login(self):
        self.assertEqual(self.client.get(reverse('perfil')).status_code, 302)
        self.assertEqual(self.client.get(reverse('editar_perfil')).status_code, 302)

    def test_edicion_perfil(self):
        usuario = get_user_model().objects.create_user('usuario')
        self.client.force_login(usuario)
        respuesta = self.client.post(reverse('editar_perfil'), {
            'biografia': 'Aprendiendo Django.',
            'link_web': 'https://ejemplo.com',
        })
        self.assertRedirects(respuesta, reverse('perfil'))
        self.assertEqual(Perfil.objects.get(user=usuario).biografia, 'Aprendiendo Django.')

    def test_logout_es_por_post(self):
        usuario = get_user_model().objects.create_user('usuario')
        self.client.force_login(usuario)
        self.assertEqual(self.client.get(reverse('logout')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('logout')), reverse('lista_posts'))
