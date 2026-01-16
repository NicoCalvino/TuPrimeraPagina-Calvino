from django.urls import path
from transacciones.views import *

urlpatterns = [
    path("", TransaccionListView.as_view(), name="lista_transacciones"),
    path('cargar_compra/', TransaccionCompraCreateView.as_view(), name='nueva_compra'),
    path('cargar_saldo/', TransaccionCargaCreateView.as_view(), name='cargar_saldo'),
]