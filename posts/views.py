from django.shortcuts import render


def inicio(request):
    return render(request, 'posts/inicio.html')


def acerca(request):
    return render(request, 'posts/acerca.html')


def lista_posts(request):
    # Por ahora los posts están cargados a mano en una lista.
    # Cuando veamos modelos, esto va a salir de la base de datos.
    posts = [
        {
            'titulo': 'Mi primer script en Python',
            'fecha': '10/08/2026',
            'resumen': 'Cómo instalé Python, configuré el entorno y escribí el clásico "Hola mundo". '
                       'Parece poco, pero ahí entendí cómo se ejecuta un programa desde la consola.',
        },
        {
            'titulo': 'Del menú por consola a los objetos',
            'fecha': '02/09/2026',
            'resumen': 'El blog empezó como un menú en la terminal. Después lo pasé a funciones, '
                       'lo separé en módulos y terminé usando clases y un archivo JSON para guardar los datos.',
        },
        {
            'titulo': 'Primeros pasos con Django',
            'fecha': '21/09/2026',
            'resumen': 'Creé el proyecto, la app posts y configuré el idioma y la zona horaria. '
                       'Ahora el blog ya se ve en el navegador con templates y CSS.',
        },
    ]
    return render(request, 'posts/lista_posts.html', {'posts': posts})
