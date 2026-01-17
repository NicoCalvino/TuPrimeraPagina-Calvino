from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.urls import reverse_lazy
from django.db import transaction
from transacciones.models import Transaccion
from kiosco.models import Tarjeta
from transacciones.forms import *
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class TransaccionListView(SuperUserRequiredMixin, ListView):
    model=Transaccion
    template_name = "transacciones/lista_transacciones.html"
    context_object_name= "transacciones"

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha')
        filtro_tipo = self.request.GET.get('concepto', 'todo')
        if filtro_tipo == 'carga':
            queryset = queryset.filter(concepto="CARGA SALDO")
        elif filtro_tipo == 'compra':
            queryset = queryset.filter(concepto="COMPRA")

        return queryset

class TransaccionDetailView(SuperUserRequiredMixin, DetailView):
    model = Transaccion
    template_name = "transacciones/ver_transaccion.html"
    context_object_name = "transaccion"
    slug_field ="id"
    slug_url_kwarg = "id"
    
class TransaccionCompraCreateView(SuperUserRequiredMixin, CreateView):
    model = Transaccion
    template_name = "transacciones/cargar_transaccion.html"
    form_class = TransaccionCompraForm
    success_url = reverse_lazy('nueva_compra')

    extra_context = {
        'titulo_pagina': 'Registrar Nueva Compra',
        'subtitulo':'Nueva Compra',
        'texto_boton': 'Confirmar Compra',
        'tipo': 'Compra',  # Útil para condicionales if/else
        'color_boton': 'btn-primary'
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.concepto = "COMPRA"

        if 'tarjeta_objeto' in form.cleaned_data:
            tarjeta = form.cleaned_data['tarjeta_objeto']
            nuevo_saldo = form.cleaned_data['nuevo_saldo_tarjeta']

            tarjeta.saldo = nuevo_saldo
            tarjeta.save()

            self.object.tarjeta = tarjeta
        
        self.object.save()

        return super().form_valid(form)
    
class TransaccionCargaCreateView(SuperUserRequiredMixin, CreateView):
    model = Transaccion
    template_name = "transacciones/cargar_transaccion.html"
    form_class = TransaccionCargaForm
    success_url = reverse_lazy('cargar_saldo')

    extra_context = {
        'titulo_pagina': 'Registrar Nueva Carga de Saldo',
        'subtitulo':'Nueva Compra',
        'texto_boton': 'Cargar Saldo',
        'tipo': 'Carga',
        'color_boton': 'btn-success' # Un verde para cargas, por ejemplo
    }

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.concepto = "CARGA SALDO"

        if 'tarjeta_objeto' in form.cleaned_data:
            tarjeta = form.cleaned_data['tarjeta_objeto']
            nuevo_saldo = form.cleaned_data['nuevo_saldo_tarjeta']

            tarjeta.saldo = nuevo_saldo
            tarjeta.save()

            self.object.tarjeta = tarjeta
        
        self.object.save()

        return super().form_valid(form)
    
class TransaccionUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Transaccion
    template_name = "transacciones/editar_transaccion.html"
    form_class = TransaccionUpdateForm
    success_url = reverse_lazy('lista_transacciones')
    slug_field ="id"
    slug_url_kwarg = "id"

    def form_valid(self, form):
        self.object = form.save(commit=False)

        if 'tarjeta_objeto' in form.cleaned_data:
            tarjeta = form.cleaned_data['tarjeta_objeto']
            nuevo_saldo = form.cleaned_data['nuevo_saldo_tarjeta']

            tarjeta.saldo = nuevo_saldo
            tarjeta.save()

            self.object.tarjeta = tarjeta
        
        self.object.save()

        return super().form_valid(form)
    
class TransaccionDeleteView(SuperUserRequiredMixin, DeleteView):
    model = Transaccion
    template_name = "transacciones/confirmar_eliminar.html"
    success_url = reverse_lazy("lista_transacciones")

    def form_valid(self, form):
        transaccion = self.get_object()
        
        tarjeta = transaccion.tarjeta

        with transaction.atomic():
            if transaccion.concepto == "CARGA SALDO":
                tarjeta.saldo -= transaccion.monto
            else:
                tarjeta.saldo += transaccion.monto
            
            tarjeta.save()

            return super().form_valid(form)