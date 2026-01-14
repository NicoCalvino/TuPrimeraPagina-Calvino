from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from users.forms import *

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
def perfil_detail(request):
    return render(request, "users/perfil_detail.html", {"user": request.user})

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