from django.shortcuts import render, redirect
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.db.models import Q
from django.db import transaction
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from transacciones.models import Transaccion, SolicitudCarga, DetalleCarga
from transacciones.forms import *

from kiosco.models import Tarjeta, Cliente

import pdb

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
        'tipo': 'Compra',
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

    extra_context = {
        'titulo_pagina': 'Registrar Nueva Carga de Saldo',
        'subtitulo':'Cargar Saldo',
        'texto_boton': 'Cargar Saldo',
        'tipo': 'Carga',
        'color_boton': 'btn-success'
    }

    def get_success_url(self):
        return reverse('ver_tarjeta', args=[self.object.tarjeta.pk])

    def get_initial(self):
        initial = super().get_initial()
        
        tarjeta_codigo = self.request.GET.get('tarjeta_codigo')
        
        if tarjeta_codigo:
            initial['numero_tarjeta'] = tarjeta_codigo
            
        return initial

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
        
class SolicitudDeCargaCreateView(LoginRequiredMixin, CreateView):
    model = SolicitudCarga
    form_class = SolicitudCargaForm
    template_name = 'transacciones/cargar_saldo_usuario.html'
    success_url = reverse_lazy('lista_solicitudes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tarjetas'] = Tarjeta.objects.filter(
            cliente__usuario = self.request.user, 
        ).select_related('cliente')
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                self.object = form.save(commit=False)
                self.object.usuario = self.request.user
                self.object.monto = 0
                self.object.save()

                tarjetas = Tarjeta.objects.filter(
                    cliente__usuario=self.request.user
                ).select_related('cliente')

                monto_total_cargado = 0

                for tarjeta in tarjetas:
 
                    input_name = f"monto_{tarjeta.id}"
                    monto = self.request.POST.get(input_name)
                    if monto and float(monto) > 0:
                        DetalleCarga.objects.create(
                            solicitud=self.object,
                            tarjeta=tarjeta,
                            monto=monto
                        )
                        monto_total_cargado += float(monto)
                
                if monto_total_cargado == 0:
                    raise ValueError("Debe ingresar un monto para al menos un alumno.")
                
                self.object.monto = monto_total_cargado
                self.object.save()

            messages.success(self.request, 'Solicitud enviada correctamente. Esperando aprobación.')
            return super().form_valid(form)
        
        except ValueError as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, "Ocurrió un error inesperado al procesar la solicitud.")
            return self.form_invalid(form)
        
class SolicitudDeCargaListView(LoginRequiredMixin, ListView):
    model=SolicitudCarga
    template_name = "transacciones/solicitudes_de_carga.html"
    context_object_name= "solicitudes"

    def get_queryset(self):
        queryset = super().get_queryset().order_by('-fecha')

        if not self.request.user.is_superuser:
            queryset = queryset.filter(usuario=self.request.user)
        filtro_tipo = self.request.GET.get('estado', 'todas')
        if filtro_tipo == 'aprobada':
            queryset = queryset.filter(estado="APROBADA")
        elif filtro_tipo == 'rechazada':
            queryset = queryset.filter(estado="RECHAZADA")
        elif filtro_tipo == 'pendiente':
            queryset = queryset.filter(estado="PENDIENTE")

        return queryset
    
class SolicitudDeCargaDetailView(LoginRequiredMixin, DetailView):
    model=SolicitudCarga
    template_name = "transacciones/detalle_solicitud_de_carga.html"
    context_object_name= "solicitud"
    slug_field ="code"
    slug_url_kwarg = "code"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.object
        detalles_carga = DetalleCarga.objects.filter(solicitud=solicitud)
        context['detalles_carga'] = detalles_carga
        
        return context
    
class SolicitudDeCargaDeleteView(LoginRequiredMixin, DeleteView):
    model = SolicitudCarga
    template_name = "transacciones/confirmar_eliminar_carga_de_saldo.html"
    context_object_name= "solicitud"
    success_url = reverse_lazy("lista_solicitudes")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitud = self.object
        detalles_carga = DetalleCarga.objects.filter(solicitud=solicitud)
        context['detalles_carga'] = detalles_carga
        
        return context
    
class SolicitudDeCargaUpdateView(SuperUserRequiredMixin, UpdateView):
    model = SolicitudCarga
    template_name = "transacciones/aprobar_rechazar_solicitud.html"
    success_url = reverse_lazy('lista_transacciones')
    slug_field = 'code'
    slug_url_kwarg = 'code'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['accion'] = self.kwargs.get('accion')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        accion = self.kwargs.get('accion')

        if accion == 'aprobar':
            self.object.estado = 'APROBADA'
            messages.success(request, f"La solicitud {self.object.code} ha sido aprobada con éxito.")
        
        elif accion == 'rechazar':
            self.object.estado = 'RECHAZADA'
            messages.warning(request, f"La solicitud {self.object.code} ha sido rechazada.")

        self.object.save()