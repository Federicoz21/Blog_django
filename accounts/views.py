from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import PerfilForm, RegistroForm
from .models import Perfil


def registro(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            Perfil.objects.create(user=usuario)
            messages.success(request, 'Cuenta creada. Ya podés iniciar sesión.')
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def perfil(request):
    datos, _ = Perfil.objects.get_or_create(user=request.user)
    return render(request, 'accounts/perfil.html', {'perfil': datos})


@login_required
def editar_perfil(request):
    datos, _ = Perfil.objects.get_or_create(user=request.user)
    avatar_anterior = datos.avatar.name

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=datos)
        if form.is_valid():
            datos = form.save()
            if avatar_anterior and avatar_anterior != datos.avatar.name:
                datos.avatar.storage.delete(avatar_anterior)
            messages.success(request, 'Tu perfil se actualizó.')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=datos)

    return render(request, 'accounts/editar_perfil.html', {
        'form': form,
        'perfil': datos,
    })
