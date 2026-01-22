from django.urls import path
from transacciones.views import *

urlpatterns = [
    path("", TransaccionListView.as_view(), name="lista_transacciones"),
    path('cargar_compra/', TransaccionCompraCreateView.as_view(), name='nueva_compra'),
    path('cargar_saldo/', TransaccionCargaCreateView.as_view(), name='cargar_saldo'),
    path('ver_transaccion/<slug:id>', TransaccionDetailView.as_view(), name='ver_transaccion'),
    path('editar_transaccion/<slug:id>', TransaccionUpdateView.as_view(), name='editar_transaccion'),
    path('<int:pk>/eliminar', TransaccionDeleteView.as_view(), name='eliminar_transaccion'),

    path('solicitud_de_carga/', SolicitudDeCargaCreateView.as_view(), name='solicitud_de_carga'),
    path('lista_solicitudes/', SolicitudDeCargaListView.as_view(), name='lista_solicitudes'),
    path('detalle_solicitud_de_carga/<slug:code>/', SolicitudDeCargaDetailView.as_view(), name='detalle_solicitud_de_carga'),
    path('editar_solicitud_de_carga/<slug:code>/', SolicitudDeCargaUpdateView.as_view(), name='editar_solicitud'),
    path('gestionar_solicitud/<slug:code>/', GestionarSolicitudView.as_view(), name='gestionar_solicitud'),
    path('eliminar_solicitud_de_carga/<int:pk>', SolicitudDeCargaDeleteView.as_view(), name='eliminar_solicitud_de_carga'),
]