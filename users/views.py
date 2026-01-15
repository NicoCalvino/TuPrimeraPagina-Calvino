from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from users.forms import *
from users.models import *

@user_passes_test(lambda u: u.is_superuser)
def lista_usuarios(request):
    busqueda = request.GET.get("buscador") 
    usuarios_query = Perfil.objects.all()
    if busqueda:
        usuarios_query = Perfil.objects.filter(
            Q(first_name__icontains = busqueda) | Q(last_name__icontains=busqueda) | Q(username__icontains=busqueda) | Q(email__icontains=busqueda),
        )
    return render(request, 'users/lista_usuarios.html',{"usuarios":usuarios_query})


def register(request):
    if request.method == "POST":
        form = PerfilCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('perfil_detail')
    else:
        form = PerfilCreateForm()
    return render(request, "users/register.html", {"form": form})

@login_required
def perfil_detail(request, pk=None):
    if pk is None:
        user_profile= request.user
    else:
        user_profile = get_object_or_404(Perfil, pk=pk)

        if not request.user.is_superuser and user_profile != request.user:
            raise PermissionDenied

    return render(request, "users/perfil_detail.html", {"user_profile": user_profile})

@login_required
def perfil_change(request):
    if request.method == "POST":
        form = PerfilChangeForm(request.POST, request.FILES, instance = request.user)
        if form.is_valid():
            form.save()
            return redirect('perfil_detail')
    else:
        form = PerfilChangeForm(instance = request.user)
    
    return render(request, "users/perfil_change.html",{"form": form})

@login_required
def confirmar_logout(request):
    return render(request, "users/logout.html", {"user": request.user})