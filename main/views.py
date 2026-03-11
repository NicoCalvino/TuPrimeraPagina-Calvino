from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from kiosco.models import *

# Vistas Básicas
def home(request):
    clientes =  Cliente.objects.none()
    if not request.user.is_authenticated:
        return render(request, "main/index_guest.html")
    
    clientes = Cliente.objects.filter(usuario=request.user)

    if request.user.is_superuser:
        return render(request, "main/index_admin.html")
    
    return render(request, "main/index.html", {'clientes': clientes})

@user_passes_test(lambda u: u.is_superuser)
def resultado_importacion(request):
    resumen = request.session.get('ultimo_resultado_importacion')
    
    if not resumen:
        return redirect('lista_usuarios') # O a una página de inicio
    
    # Limpiamos la sesión después de leerla para que no aparezca de nuevo al refrescar
    # del request.session['ultimo_resultado_importacion'] 
    
    return render(request, 'main/resultado_importacion.html', {'resumen': resumen})