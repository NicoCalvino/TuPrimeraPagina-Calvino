from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Right 
from django.core.paginator import Paginator
from django.contrib import messages
from kiosco.models import *
from kiosco.forms import *
from transacciones.models import *
from django.contrib.auth.decorators import login_required, user_passes_test

# Vistas Básicas
def home(request):
    clientes =  Cliente.objects.none()
    if request.user.is_authenticated:
        clientes = Cliente.objects.filter(usuario=request.user)

    if request.user.is_superuser:
        return render(request, "kiosco/index_admin.html")
    
    return render(request, "kiosco/index.html", {'clientes': clientes})

def about_me(request):
    return render(request, "kiosco/acerca_de_mi.html")

# Vistas de Clientes
## Lista de Clientes
@user_passes_test(lambda u: u.is_superuser)
def lista_clientes(request):
    busqueda = request.GET.get("nombre") 
    orden = request.GET.get('orden')
    clientes_query = Cliente.objects.all()
    if busqueda:
        clientes_query = Cliente.objects.filter(
            Q(nombre__icontains = busqueda) | Q(apellido__icontains=busqueda) | Q(usuario__first_name__icontains=busqueda) | Q(usuario__last_name__icontains=busqueda),
        )
    
    if orden == 'apellido':
        clientes_query = clientes_query.order_by('apellido')
    elif orden == 'curso':
        clientes_query = clientes_query.order_by('curso')
    elif orden == 'tutor':
        clientes_query = clientes_query.order_by('usuario')

    return render(request, 'kiosco/clientes.html',{"clientes":clientes_query})

## Creacion de Clientes
@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect("home")
    else:
        form = ClienteForm()

    return render(request, 'kiosco/crear_cliente.html', {'form':form})

## Ver detalle de Cliente
@login_required
def ver_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.usuario != request.user:
        messages.error(request, 'No tienes permiso para ver ese cliente.')
        return redirect('home')
    return render(request, 'kiosco/ver_cliente.html', {"cliente":cliente})

## Actualizar informacion de Cliente
@login_required
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar ese cliente.')
        return redirect('home')
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("ver_cliente",pk = cliente.pk)
    else:
        form = ClienteForm(instance=cliente)

    return render(request, "kiosco/editar_cliente.html",{
        "form":form,
        "cliente":cliente        
    })

## Eliminar Cliente
@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.usuario != request.user:
        messages.error(request, 'No tienes permiso para editar ese cliente.')
        return redirect('home')
    if request.method == "POST":
        cliente.delete()
        return redirect('home')
    return render(request, "kiosco/eliminar_cliente.html",{
        "cliente":cliente
    })

## Historial completo de transacciones de Cliente
@login_required
def historial_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if cliente.usuario != request.user:
        messages.error(request, 'No tienes permiso para ver el historial de ese cliente.')
        return redirect('home')
    movimientos_list = Transaccion.objects.filter(tarjeta__cliente=cliente).order_by('-fecha')
    
    paginator = Paginator(movimientos_list, 20)
    page_number = request.GET.get('page')
    movimientos = paginator.get_page(page_number)
    
    return render(request, 'kiosco/historial_completo_cliente.html', {
        'cliente': cliente,
        'movimientos': movimientos, 
        'page_obj': movimientos,    
        'is_paginated': True
    })

# Vistas de Tarjetas
## Lista de Tarjetas
@user_passes_test(lambda u: u.is_superuser)
def lista_tarjetas(request):
    codigo = request.GET.get("codigo") 
    tarjetas_query = Tarjeta.objects.all()

    filtro = request.GET.get('filtro')
    if filtro == 'con_usuario':
        tarjetas_query = tarjetas_query.exclude(cliente__isnull=True)
    elif filtro == 'sin_usuario':
        tarjetas_query = tarjetas_query.filter(cliente__isnull=True)
    
    if codigo:
        tarjetas_query = tarjetas_query.annotate(
            ultimos_digitos=Right('codigo', 9)
        ).filter(
            ultimos_digitos__icontains=codigo
        )
    return render(request, 'kiosco/tarjetas.html',{"tarjetas":tarjetas_query})

## Creacion de Tarjetas
@user_passes_test(lambda u: u.is_superuser)
def crear_tarjeta(request):
    if request.method == "POST":
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_tarjetas")
    else:
        form = TarjetaForm()

    return render(request, 'kiosco/crear_tarjeta.html', {'form':form})

## Ver detalle de Tarjeta
@user_passes_test(lambda u: u.is_superuser)
def ver_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    return render(request, 'kiosco/ver_tarjeta.html', {'tarjeta':tarjeta})

## Eliminar Tarjeta
@user_passes_test(lambda u: u.is_superuser)
def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if request.method == "POST":
        tarjeta.delete()
        return redirect('lista_tarjetas')
    return render(request, "kiosco/eliminar_tarjeta.html",{
        "tarjeta":tarjeta
    })

## Asociar Tarjeta a cliente
@user_passes_test(lambda u: u.is_superuser)
def asociar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    busqueda_cliente = request.GET.get("nombre") 
    clientes_query = Cliente.objects.all()
    if busqueda_cliente:
        clientes_query = Cliente.objects.filter(
            Q(nombre__icontains = busqueda_cliente) | Q(apellido__icontains=busqueda_cliente),
        )

    return render(request, 'kiosco/asociar_cliente_lista.html', {
        'tarjeta': tarjeta,
        'clientes': clientes_query,
        'query': busqueda_cliente
    })

## Confirmar Asociación de tarjeta
@user_passes_test(lambda u: u.is_superuser)
def asociar_tarjeta_confirmar(request, pk, cliente_pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    cliente = get_object_or_404(Cliente, pk=cliente_pk)

    if request.method == 'POST':
        tarjeta.cliente = cliente
        tarjeta.save()

        return redirect('ver_tarjeta', pk=tarjeta.pk)
    
    return render(request, 'kiosco/asociar_cliente_confirmar.html', {
        'tarjeta': tarjeta,
        'cliente': cliente
    })

## Habilitar o Deshabilitar Tarjeta desde para Superuser
@user_passes_test(lambda u: u.is_superuser)
def cambiar_estado_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    tarjeta.habilitada = not tarjeta.habilitada 
    tarjeta.save()

    return redirect('ver_tarjeta', tarjeta.pk)

## Habilitar o Deshabilitar Tarjeta desde el usuario común
@login_required
def cambiar_estado_tarjeta_alumno(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if tarjeta.cliente.usuario != request.user:
        messages.error(request, 'No puedes modificar esa tarjeta')
        return redirect('home')
    tarjeta.habilitada = not tarjeta.habilitada 
    tarjeta.save()

    return redirect('ver_cliente', pk=tarjeta.cliente.pk)


