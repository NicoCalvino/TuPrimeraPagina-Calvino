from django.urls import path
from productos.views import *

urlpatterns = [
    path("", ProductoListView.as_view(), name="lista_productos"),
    path("crear/", ProductoCreateView.as_view(), name="crear_producto"),
    path("<slug:code>/", ProductoDetailView.as_view(), name="detalle_producto"),
    path("<slug:code>/editar", ProductoUpdateView.as_view(), name="editar_producto"),
    path("<int:pk>/eliminar", ProductoDeleteView.as_view(), name="eliminar_producto"),
]