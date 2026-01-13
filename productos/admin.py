from django.contrib import admin
from productos.models import *

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre","marca", "categoria", "precio","stock", "codigo_de_barras","code")
    list_display_links = ("nombre",)
    search_fields = ("nombre","marca","categoria","codigo_de_barras")
    ordering = ("categoria", "nombre","marca")