import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .forms import PostForm
from .models import Post

# Las imágenes de los tests se guardan en una carpeta temporal, no en media/
MEDIA_DE_PRUEBA = tempfile.mkdtemp()


def imagen_de_prueba(nombre='foto.png', color='cyan'):
    """Arma una imagen PNG chiquita en memoria, como si la subiera un usuario."""
    archivo = BytesIO()
    Image.new('RGB', (40, 30), color).save(archivo, 'PNG')
    return SimpleUploadedFile(nombre, archivo.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_DE_PRUEBA)
class CrudPostsTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_DE_PRUEBA, ignore_errors=True)
        super().tearDownClass()

    def datos(self, **cambios):
        datos = {
            'titulo': 'Mi primer post',
            'contenido': 'Hola, este es el contenido.',
            'autor': 'Federico',
            'estado': 'publicado',
        }
        datos.update(cambios)
        return datos

    def test_el_formulario_tiene_los_campos_pedidos(self):
        self.assertEqual(
            list(PostForm().fields),
            ['titulo', 'contenido', 'autor', 'estado', 'imagen'],
        )

    def test_crear_post_con_imagen(self):
        respuesta = self.client.post(
            reverse('crear_post'),
            self.datos(imagen=imagen_de_prueba()),
        )
        post = Post.objects.get()
        self.assertRedirects(respuesta, reverse('detalle_post', args=[post.pk]))
        self.assertTrue(post.imagen.name.startswith('posts/'))
        self.assertTrue(post.imagen.storage.exists(post.imagen.name))

        # La imagen aparece en el detalle
        detalle = self.client.get(reverse('detalle_post', args=[post.pk]))
        self.assertContains(detalle, post.imagen.url)

    def test_crear_post_sin_imagen(self):
        respuesta = self.client.post(reverse('crear_post'), self.datos())
        post = Post.objects.get()
        self.assertRedirects(respuesta, reverse('detalle_post', args=[post.pk]))
        self.assertFalse(post.imagen)

        # Sin imagen el detalle no se rompe y muestra el aviso
        detalle = self.client.get(reverse('detalle_post', args=[post.pk]))
        self.assertContains(detalle, 'Este post no tiene imagen.')

    def test_un_archivo_que_no_es_imagen_se_rechaza(self):
        texto = SimpleUploadedFile('nota.png', b'esto no es una imagen', content_type='image/png')
        respuesta = self.client.post(reverse('crear_post'), self.datos(imagen=texto))
        self.assertEqual(respuesta.status_code, 200)  # vuelve a mostrar el formulario con el error
        self.assertFalse(Post.objects.exists())

    def test_el_formulario_envia_archivos(self):
        respuesta = self.client.get(reverse('crear_post'))
        self.assertContains(respuesta, 'enctype="multipart/form-data"')

    def test_editar_post_y_cambiar_la_imagen(self):
        post = Post.objects.create(**self.datos(), imagen=imagen_de_prueba('vieja.png'))
        imagen_vieja = post.imagen.name

        respuesta = self.client.post(
            reverse('editar_post', args=[post.pk]),
            self.datos(titulo='Título editado', imagen=imagen_de_prueba('nueva.png', 'magenta')),
        )
        self.assertRedirects(respuesta, reverse('detalle_post', args=[post.pk]))

        post.refresh_from_db()
        self.assertEqual(post.titulo, 'Título editado')
        self.assertIn('nueva', post.imagen.name)
        self.assertTrue(post.imagen.storage.exists(post.imagen.name))
        self.assertFalse(post.imagen.storage.exists(imagen_vieja))  # el archivo viejo se borró

    def test_editar_sin_tocar_la_imagen_la_conserva(self):
        post = Post.objects.create(**self.datos(), imagen=imagen_de_prueba())
        imagen = post.imagen.name
        self.client.post(reverse('editar_post', args=[post.pk]), self.datos(contenido='Otro texto'))
        post.refresh_from_db()
        self.assertEqual(post.imagen.name, imagen)
        self.assertTrue(post.imagen.storage.exists(imagen))

    def test_editar_y_quitar_la_imagen(self):
        post = Post.objects.create(**self.datos(), imagen=imagen_de_prueba())
        imagen = post.imagen.name
        self.client.post(
            reverse('editar_post', args=[post.pk]),
            self.datos(**{'imagen-clear': 'on'}),
        )
        post.refresh_from_db()
        self.assertFalse(post.imagen)
        self.assertFalse(post.imagen.storage.exists(imagen))

    def test_eliminar_pide_confirmacion_antes_de_borrar(self):
        post = Post.objects.create(**self.datos(), imagen=imagen_de_prueba())
        imagen = post.imagen.name
        url = reverse('eliminar_post', args=[post.pk])

        # Entrar a la página solo muestra la confirmación
        respuesta = self.client.get(url)
        self.assertContains(respuesta, 'Sí, eliminar')
        self.assertTrue(Post.objects.filter(pk=post.pk).exists())

        # Confirmar (POST) lo borra, junto con su imagen
        respuesta = self.client.post(url)
        self.assertRedirects(respuesta, reverse('lista_posts'))
        self.assertFalse(Post.objects.filter(pk=post.pk).exists())
        self.assertFalse(post.imagen.storage.exists(imagen))

    def test_la_lista_muestra_los_posts_y_sus_imagenes(self):
        con_imagen = Post.objects.create(**self.datos(titulo='Con foto'), imagen=imagen_de_prueba())
        Post.objects.create(**self.datos(titulo='Sin foto', estado='borrador'))

        respuesta = self.client.get(reverse('lista_posts'))
        self.assertContains(respuesta, 'Con foto')
        self.assertContains(respuesta, 'Sin foto')
        self.assertContains(respuesta, con_imagen.imagen.url)

    def test_un_post_que_no_existe_da_404(self):
        for nombre in ['detalle_post', 'editar_post', 'eliminar_post']:
            respuesta = self.client.get(reverse(nombre, args=[999]))
            self.assertEqual(respuesta.status_code, 404)
