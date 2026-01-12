from django.contrib import admin
from kiosco.models import *
# Register your models here.

#admin.site.register(Alumna)
#admin.site.register(Tarjeta)
#admin.site.register(Producto)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    #Columna visibles en la lista del modelo
    list_display = ("nombre", "apellido", "curso")
    #Columnas con enlaces clickeables para entrar en el detalle
    list_display_links = ("nombre",)
    #Campos por los que se puede buscar
    search_fields = ("nombre","apellido")
    #Orden por defecto
    ordering = ("apellido","nombre")
    
    
@admin.register(Tarjeta)
class TarjetaAdmin(admin.ModelAdmin):
    list_display = ("codigo","saldo","fecha_activacion","alumna")
    list_display_links = ("codigo",)
    search_fields = ("codigo","id_alumna")
    #Filtros laterales
    list_filter = ("fecha_activacion",)
    #Orden por defecto
    ordering = ("fecha_activacion","codigo")
    #Campos de solo lectura
    readonly_fields = ("fecha_activacion",)

# @admin.register(Producto)
# class ProductoAdmin(admin.ModelAdmin):
#     list_display = ("nombre","marca", "categoria", "precio","stock", "codigo_de_barras")
#     list_display_links = ("nombre",)
#     search_fields = ("nombre","marca","categoria","codigo_de_barras")
#     ordering = ("categoria", "nombre","marca")
    