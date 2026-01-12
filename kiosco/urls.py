from django.urls import path
from kiosco.views import *

urlpatterns = [
    path("",home, name="home"),

    # path("lista_productos", lista_productos, name="lista_productos"),
    # path("crear_producto", crear_producto, name="crear_producto"),
    # path("ver_producto/<int:pk>",ver_producto, name="ver_producto"),
   
    path("lista_clientes",lista_clientes, name="lista_clientes"),
    path("crear_cliente", crear_cliente, name="crear_cliente"),
    path("ver_cliente/<int:pk>",ver_cliente, name="ver_cliente"),
    path("actualizar_cliente/<int:pk>",actualizar_cliente, name="actualizar_cliente"),
    path("eliminar_cliente/<int:pk>",eliminar_cliente, name="eliminar_cliente"),

    path("lista_tarjetas",lista_tarjetas, name="lista_tarjetas"),
    path("crear_tarjeta", crear_tarjeta, name="crear_tarjeta"),
    path("ver_tarjeta/<int:pk>",ver_tarjeta, name="ver_tarjeta"),
    path("eliminar_tarjeta/<int:pk>",eliminar_tarjeta, name="eliminar_tarjeta"),
]