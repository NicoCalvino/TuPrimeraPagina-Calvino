from django.shortcuts import render
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.urls import reverse_lazy
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
    
class TransaccionCompraCreateView(SuperUserRequiredMixin, CreateView):
    model = Transaccion
    template_name = "transacciones/cargar_compra.html"
    form_class = TransaccionCompraForm
    success_url = reverse_lazy('nueva_compra')

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
    template_name = "transacciones/cargar_saldo.html"
    form_class = TransaccionCargaForm
    success_url = reverse_lazy('cargar_saldo')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.concepto = "CARGA SALDO"

        if 'tarjeta_objeto' in form.cleaned_data:
            tarjeta = form.cleaned_data['tarjeta_objeto']
            nuevo_saldo = form.cleaned_data['nuevo_saldo_tarjeta']

            tarjeta.saldo = nuevo_saldo
            tarjeta.save()

            self.object.tarjeta = tarjeta
            self.object.detalle = "CARGA DE SALDO EN TARJETA"
        
        self.object.save()

        return super().form_valid(form)