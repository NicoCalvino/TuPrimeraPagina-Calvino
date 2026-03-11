from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView, TemplateView
from django.db.models import Q, F, IntegerField
from django.db.models.functions import Cast
import pandas as pd
from comedor.models import *
from comedor.forms import *
from escuela.models import Cliente, Colegio
from users.models import Perfil
from datetime import date, datetime, timedelta

class SuperUserRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

class ComedorHomeView(SuperUserRequiredMixin, TemplateView):
    template_name = "comedor/home.html"

# Precios
class PrecioListView(SuperUserRequiredMixin, ListView):
    model = Precio
    template_name = "comedor/lista_precios.html"
    context_object_name = "precios"

    def get_queryset(self):
        return Precio.objects.all().select_related('colegio')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Enviamos todos los colegios para llenar el <select> del filtro
        context['colegios'] = Colegio.objects.all().order_by('nombre') 
        return context

class CargarPrecioView(SuperUserRequiredMixin, CreateView):
    model = Precio
    template_name = "comedor/nuevo_precio.html"
    form_class = PrecioForm
    context_object_name = "precio"

    def get_success_url(self):
        if '_addanother' in self.request.POST:
            messages.success(self.request, '¡Precio creado exitosamente! Puedes cargar el siguiente.', 
                extra_tags='mensaje_local' )
            return reverse_lazy('cargar_precio')    
        return reverse_lazy("lista_precios")

class PrecioUpdateView(SuperUserRequiredMixin, UpdateView):
    model = Precio
    template_name = "comedor/nuevo_precio.html"
    form_class = PrecioForm
    
    def get_success_url(self):
        return reverse_lazy(
            "lista_precios"
            )      

class ImportarPreciosView(SuperUserRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('archivo_excel')

        if not excel_file or not excel_file.name.endswith(('.xlsx', '.xls')):
            messages.error(request, "Por favor, sube un archivo Excel válido.")
            return redirect('lista_precios')
        
        try:
            df = pd.read_excel(excel_file)
            df = df.fillna('') # Evitar errores de NaN con strings

            resultados = {
                'exitos': 0,
                'errores': [],
                'total': len(df),
                'proceso': 'Importación de Precios',
                'url_retorno': 'lista_precios'
            }

            for index, row in df.iterrows():
                # Limpieza de datos básica
                nombre_colegio = str(row.get('colegio', '')).strip()
                alm_por_sem = str(row.get('alm_por_sem', '')).strip()
                nivel = str(row.get('nivel', '')).strip()
                nro_de_cliente = str(row.get('nro_de_cliente', '')).strip()
                precio = str(row.get('precio', '')).strip()

                try:
                    colegio_obj = Colegio.objects.get(nombre=nombre_colegio)

                    if Precio.objects.filter(
                        alm_por_sem=alm_por_sem, 
                        nivel=nivel, 
                        nro_de_cliente=nro_de_cliente, 
                        colegio=colegio_obj
                        ).exists():
                        resultados['errores'].append({
                            'fila': index + 2,
                            'identificador': f"{nivel} - {alm_por_sem} x sem - hijo nro {nro_de_cliente} - {nombre_colegio}",
                            'mensaje': "El precio ya está registrado."
                        })
                        continue

                    Precio.objects.create(
                        alm_por_sem=alm_por_sem,
                        nro_de_cliente=nro_de_cliente,
                        nivel=nivel,
                        precio=precio,
                        colegio=colegio_obj,
                    )
                    resultados['exitos'] += 1
                
                except Exception as e:
                    resultados['errores'].append({
                        'fila': index + 2,
                        'identificador': f"{nivel} - {alm_por_sem} x sem - hijo nro {nro_de_cliente} - {nombre_colegio}",
                        'mensaje': str(e)
                    })

            request.session['ultimo_resultado_importacion'] = resultados
            return redirect('resultado_importacion')

        except Exception as e:
            messages.error(request, f"Error crítico: {e}")
            return redirect('lista_precios')
    
    def get(self, request, *args, **kwargs):
        return redirect('lista_precios')

# Vale Mensual
class ComedorMensualView(SuperUserRequiredMixin, ListView):
    model = ValeMensual
    template_name = "comedor/comedor_mensual.html"
    context_object_name = "vales"

    def get_queryset(self):
        return super().get_queryset()

class CargarValeMensualView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ValeMensual
    template_name = "comedor/vale_mensual.html"
    form_class = ValeMensualForm
    context_object_name = "vale_mensual"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        
        return cliente.usuario == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        context['cliente'] = cliente
        
        context['precios_escuela_uno'] = Precio.objects.filter(
            nivel="PRIMARIA/SECUNDARIA",
            nro_de_cliente = 1,
            colegio=cliente.curso.colegio
        ).order_by('alm_por_sem')

        context['precios_escuela_dos'] = Precio.objects.filter(
            nivel="PRIMARIA/SECUNDARIA",
            nro_de_cliente = 2,
            colegio=cliente.curso.colegio
        ).order_by('alm_por_sem')

        context['precios_escuela_tres'] = Precio.objects.filter(
            nivel="PRIMARIA/SECUNDARIA",
            nro_de_cliente = 3,
            colegio=cliente.curso.colegio
        ).order_by('alm_por_sem')
        
        context['precios_jardin'] = Precio.objects.filter(
            nivel="JARDIN",
            colegio=cliente.curso.colegio,
        ).order_by('alm_por_sem')

        return context
    
    def form_valid(self, form):
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        
        form.instance.cliente = cliente
        form.instance.usuario = self.request.user # O ajustalo según cómo se llame tu relación de perfil
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ver_cliente', kwargs={'pk': self.kwargs['pk']})
    
class ActualizarValeMensualView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = ValeMensual
    template_name = "comedor/vale_mensual.html"
    form_class = ValeMensualForm

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        
        vale_mensual = self.get_object()
        
        return vale_mensual.usuario == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cliente'] = self.object.cliente 
        return context

    def get_success_url(self):
        return reverse_lazy('ver_cliente', kwargs={'pk': self.object.cliente.pk})
    

# Vale Diario
class ComedorDiarioView(SuperUserRequiredMixin,ListView):
    model = ValeDiario
    template_name = "comedor/lista_vales_diarios.html"
    context_object_name = "vales"

    def get_queryset(self):
        return super().get_queryset()

class CargarValeDiarioView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ValeDiario
    template_name = "comedor/vale_diario.html"
    form_class = ValeDiarioForm
    context_object_name = "vale_diario"

    def test_func(self):
        if self.request.user.is_superuser:
            return True
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        return cliente.usuario == self.request.user

    def get_form_kwargs(self):
            kwargs = super().get_form_kwargs()
            kwargs['cliente_id'] = self.kwargs.get('pk')
            return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        context['cliente'] = cliente
        context['fecha_minima'] = date.today().strftime('%Y-%m-%d')

        pj = Precio.objects.filter(
            alm_por_sem=1,
            nivel="JARDIN",
            colegio=cliente.curso.colegio
        ).first()
        context['precio_jardin'] = pj.precio / 4 if pj else 0

        pe = Precio.objects.filter(
            alm_por_sem=1,
            nivel="PRIMARIA/SECUNDARIA",
            colegio=cliente.curso.colegio
        ).first()
        context['precio_escuela'] = pe.precio / 4 if pe else 0

        return context
    
    def form_valid(self, form):
        cliente = get_object_or_404(Cliente, pk=self.kwargs['pk'])
        
        form.instance.cliente = cliente
        form.instance.usuario = self.request.user # O ajustalo según cómo se llame tu relación de perfil
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('ver_cliente', kwargs={'pk': self.kwargs['pk']})
    
class CancelarValeDiarioView(LoginRequiredMixin, View):
    
    def post(self, request, pk):
        vale = get_object_or_404(ValeDiario, pk=pk)
        vale.cancelado = True
        vale.save()
        
        return redirect('ver_cliente', pk=vale.cliente.pk)
    
class HistorialValesDiariosView(LoginRequiredMixin, ListView):
    model = ValeDiario
    template_name = "comedor/historial_vales_diarios.html"
    context_object_name = "vales"

    def get_queryset(self):
        cliente_id = self.kwargs.get('pk')
        return ValeDiario.objects.filter(cliente_id=cliente_id).order_by('-fecha')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pasamos el cliente al HTML para poder poner su nombre en el título
        context['cliente'] = get_object_or_404(Cliente, pk=self.kwargs.get('pk'))
        context['hoy'] = date.today() 
        return context

# Reportes
class ReporteDiarioView(TemplateView):
    template_name = 'comedor/reporte_diario.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 1. Determinar la fecha objetivo
        ahora = timezone.localtime(timezone.now())
        if ahora.hour >= 15:
            fecha_consulta = ahora.date() + timedelta(days=1)
        else:
            fecha_consulta = ahora.date()

        # 2. Mapeo de días de la semana para el modelo ValeMensual
        # weekday() devuelve 0 para Lunes, 1 Martes...
        dias_mapeo = {
            0: 'lunes',
            1: 'martes',
            2: 'miercoles',
            3: 'jueves',
            4: 'viernes',
        }
        dia_semana_num = fecha_consulta.weekday()
        nombre_campo_dia = dias_mapeo.get(dia_semana_num)

        lista_asistencia = []

        # 3. Obtener alumnos por Vale Mensual (si no es fin de semana)
        if nombre_campo_dia:
            # Filtramos dinámicamente por el nombre del campo (ej: lunes=True)
            filtro_mensual = {f"{nombre_campo_dia}": True}
            mensuales = ValeMensual.objects.filter(**filtro_mensual).select_related('cliente')
            
            for vale in mensuales:
                lista_asistencia.append({
                    'cliente': vale.cliente,
                    'origen': 'Plan Mensual',
                    'comentarios': vale.comentarios
                })
        
        # 4. Obtener alumnos por Vale Diario
        diarios = ValeDiario.objects.filter(
            fecha=fecha_consulta, 
            cancelado=False
        ).select_related('cliente')

        for vale in diarios:
            # Evitar duplicados si el alumno tiene mensual y además sacó diario
            if not any(item['cliente'] == vale.cliente for item in lista_asistencia):
                lista_asistencia.append({
                    'cliente': vale.cliente,
                    'origen': 'Vale Diario',
                    'comentarios': 'N/A'
                })
        

        # Ordenar por curso o nombre si se desea
        lista_asistencia.sort(key=lambda x: (x['cliente'].curso.curso, x['cliente'].nombre))

        context['lista_asistencia'] = lista_asistencia
        context['fecha_consulta'] = fecha_consulta
        return context
    
class ReporteFacturacionView(ListView):
    model = Perfil
    template_name = 'comedor/reporte_mensual.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        # Traemos solo perfiles que tienen vales mensuales activos
        return Perfil.objects.filter(valemensual__isnull=False).distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reporte = []

        for usuario in self.get_queryset():
            # Optimizamos la consulta con select_related para evitar el problema N+1
            vales = ValeMensual.objects.filter(usuario=usuario).select_related(
                'cliente', 'cliente__curso'
            ).order_by('cliente__nombre')
            
            datos_usuario = {
                'padre': usuario,
                'hijos': [],
                'total_padre': 0
            }

            vales = vales.annotate(
                total_dias=Cast(
                    F('lunes') + F('martes') + F('miercoles') + F('jueves') + F('viernes'),
                    output_field=IntegerField()
                )
            ).order_by('-total_dias')


            for indice, vale in enumerate(vales, start=1):
                # Calcular días marcados (sumamos los valores booleanos)
                vale.dias_semana = sum([
                    vale.lunes, vale.martes, vale.miercoles, 
                    vale.jueves, vale.viernes
                ])
                
                if vale.dias_semana == 0:
                    continue

                # Lógica de descuento familiar: tope en el 3er hijo (según tabla de precios)
                nro_hijo_clave = indice if indice <= 3 else 3
                
                # Accedemos a la escuela a través de la relación Cliente -> Curso
                tipo_escuela = vale.cliente.curso.escuela
                
                # Buscamos el precio correspondiente en la base de datos
                precio_obj = Precio.objects.filter(
                    alm_por_sem=vale.dias_semana,
                    escuela=tipo_escuela,
                    nro_de_cliente=nro_hijo_clave
                ).first()
                
                precio_monto = precio_obj.precio if precio_obj else 0
                
                datos_usuario['hijos'].append({
                    'nombre': f"{vale.cliente.nombre} {vale.cliente.apellido}",
                    'curso': vale.cliente.curso.curso,
                    'escuela': tipo_escuela,
                    'dias': vale.dias_semana,
                    'nro_orden': indice,
                    'subtotal': precio_monto
                })
                
                datos_usuario['total_padre'] += precio_monto
                
            if datos_usuario['hijos']:
                reporte.append(datos_usuario)

        context['reporte'] = reporte
        return context