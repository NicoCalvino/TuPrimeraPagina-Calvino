from django.urls import path
from transacciones.views import *

urlpatterns = [
    path("", TransaccionListView.as_view(), name="lista_transacciones"),
    path('cargar_compra/', TransaccionCompraCreateView.as_view(), name='nueva_compra'),
    path('cargar_saldo/', TransaccionCargaCreateView.as_view(), name='cargar_saldo'),
    path('ver_transaccion/<slug:id>', TransaccionDetailView.as_view(), name='ver_transaccion'),
    path('editar_transaccion/<slug:id>', TransaccionUpdateView.as_view(), name='editar_transaccion'),
    path('<int:pk>/eliminar', TransaccionDeleteView.as_view(), name='eliminar_transaccion'),
]