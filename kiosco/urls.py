from django.urls import path
from kiosco.views import *

urlpatterns = [
    path("",home, name="home"),

    path("lista_productos", lista_productos, name="lista_productos"),
    path("crear_producto", crear_producto, name="crear_producto"),
    path("ver_producto/<int:pk>",ver_producto, name="ver_producto"),
   
    path("lista_alumnas",lista_alumnas, name="lista_alumnas"),
    path("crear_alumna", crear_alumna, name="crear_alumna"),
    path("ver_alumna/<int:pk>",ver_alumna, name="ver_alumna"),

    path("lista_tarjetas",lista_tarjetas, name="lista_tarjetas"),
    path("crear_tarjeta", crear_tarjeta, name="crear_tarjeta"),
    path("ver_tarjeta/<int:pk>",ver_tarjeta, name="ver_tarjeta"),
]