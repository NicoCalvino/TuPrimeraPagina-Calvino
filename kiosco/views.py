from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.db.models.functions import Right 
from kiosco.models import *
from kiosco.forms import *
from decimal import Decimal
from django.contrib.auth.decorators import login_required, user_passes_test

def home(request):
    clientes =  Cliente.objects.none()
    if request.user.is_authenticated:
        clientes = Cliente.objects.filter(usuario=request.user)
    
    return render(request, "kiosco/index.html", {'clientes': clientes})


# Clientes
@user_passes_test(lambda u: u.is_superuser)
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
            cliente = form.save(commit=False)
            cliente.usuario = request.user
            cliente.save()
            return redirect("home")
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
        return redirect('home')
    return render(request, "kiosco/eliminar_cliente.html",{
        "cliente":cliente
    })

# Tarjetas
@user_passes_test(lambda u: u.is_superuser)
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

@user_passes_test(lambda u: u.is_superuser)
def ver_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    return render(request, 'kiosco/ver_tarjeta.html', {'tarjeta':tarjeta})

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



# @user_passes_test(lambda u: u.is_superuser)
# def actualizar_tarjeta(request, pk):
#     tarjeta = get_object_or_404(Tarjeta, pk=pk)
#     if request.method == "POST":
#         monto_str = request.POST.get("monto")
#         if monto_str:
#             try:
#                 monto_a_sumar = Decimal(monto_str)
#                 tarjeta.saldo += monto_a_sumar
#                 tarjeta.save()

#                 return redirect("ver_tarjeta",pk = tarjeta.pk)
#             except ValueError:
#                 form = TarjetaSaldoForm(instance=tarjeta)
#     else:
#         form = TarjetaSaldoForm(instance=tarjeta)

#     return render(request, "kiosco/saldo_tarjeta.html",{
#         "form":form,
#         "tarjeta":tarjeta        
#     })

@user_passes_test(lambda u: u.is_superuser)
def eliminar_tarjeta(request, pk):
    tarjeta = get_object_or_404(Tarjeta, pk=pk)
    if request.method == "POST":
        tarjeta.delete()
        return redirect('lista_tarjetas')
    return render(request, "kiosco/eliminar_tarjeta.html",{
        "tarjeta":tarjeta
    })