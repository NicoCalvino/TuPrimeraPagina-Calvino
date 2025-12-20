from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Right 
from kiosco.models import *
from kiosco.forms import *

def home(request):
    return render(request, "kiosco/index.html")


# Productos
def lista_productos(request):
    busqueda = request.GET.get("nombre") 
    productos_query = Producto.objects.all()
    if busqueda:
        productos_query = Producto.objects.filter(
            Q(nombre__icontains = busqueda) | Q(marca__icontains=busqueda) | Q(categoria__icontains=busqueda),
        )
    return render(request, 'kiosco/productos.html',{"productos":productos_query})

def crear_producto(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_productos")
    else:
        form = ProductoForm()

    return render(request, 'kiosco/crear_producto.html', {'form':form})

def ver_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'kiosco/ver_producto.html', {"producto":producto})

# Alumnas
def lista_alumnas(request):
    busqueda = request.GET.get("nombre") 
    alumnas_query = Alumna.objects.all()
    if busqueda:
        alumnas_query = Alumna.objects.filter(
            Q(nombre__icontains = busqueda) | Q(apellido__icontains=busqueda),
        )
    return render(request, 'kiosco/alumnas.html',{"alumnas":alumnas_query})

def crear_alumna(request):
    if request.method == "POST":
        form = AlumnaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_alumnas")
    else:
        form = AlumnaForm()

    return render(request, 'kiosco/crear_alumna.html', {'form':form})

def ver_alumna(request, pk):
    alumna = get_object_or_404(Alumna, pk=pk)
    return render(request, 'kiosco/ver_alumna.html', {"alumna":alumna})

# Tarjetas
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

def crear_tarjeta(request):
    if request.method == "POST":
        form = TarjetaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("lista_tarjetas")
    else:
        form = TarjetaForm()

    return render(request, 'kiosco/crear_tarjeta.html', {'form':form})

def ver_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    return render(request, 'kiosco/ver_tarjeta.html', {"tarjeta":tarjeta})

