from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Right 
from kiosco.models import *
from kiosco.forms import *
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, "kiosco/index.html")


# Clientes
@login_required
def lista_clientes(request):
    busqueda = request.GET.get("nombre") 
    clientes_query = Cliente.objects.all()
    if busqueda:
        clientes_query = Cliente.objects.filter(
            Q(nombre__icontains = busqueda) | Q(apellido__icontains=busqueda),
        )
    return render(request, 'kiosco/clientes.html',{"clientes":clientes_query})

@login_required
def crear_cliente(request):
    if request.method == "POST":
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_clientes")
    else:
        form = ClienteForm()

    return render(request, 'kiosco/crear_cliente.html', {'form':form})

@login_required
def ver_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'kiosco/ver_cliente.html', {"cliente":cliente})

@login_required
def actualizar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect("ver_cliente",pk = cliente.pk)
    else:
        form = ClienteForm(instance=cliente)
        return render(request, "kiosco/crear_cliente.html",{
            "form":form,
            "cliente":cliente        
        })

@login_required
def eliminar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == "POST":
        cliente.delete()
        return redirect('lista_clientes')
    return render(request, "kiosco/eliminar_cliente.html",{
        "cliente":cliente
    })

# Tarjetas
@login_required
def lista_tarjetas(request):
    codigo = request.GET.get("codigo") 
    tarjetas_query = Tarjeta.objects.all()
    if codigo:
        tarjetas_query = tarjetas_query.annotate(
            ultimos_digitos=Right('codigo', 9)
        ).filter(
            ultimos_digitos__icontains=codigo
        )
    return render(request, 'kiosco/tarjetas.html',{"tarjetas":tarjetas_query})

@login_required
def crear_tarjeta(request):
    if request.method == "POST":
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_tarjetas")
    else:
        form = TarjetaForm()

    return render(request, 'kiosco/crear_tarjeta.html', {'form':form})

@login_required
def ver_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    return render(request, 'kiosco/ver_tarjeta.html', {"tarjeta":tarjeta})

@login_required
def actualizar_tarjeta(request, pk):
    pass # NO SE CONSIDERA NECESARIO EDITAR LA INFORMACION DE LAS TARJETAS AUN

@login_required
def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if request.method == "POST":
        tarjeta.delete()
        return redirect('lista_tarjetas')
    return render(request, "kiosco/eliminar_tarjeta.html",{
        "tarjeta":tarjeta
    })