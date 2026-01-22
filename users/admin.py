from django.contrib import admin
from users.models import *
# Register your models here.

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    #Columna visibles en la lista del modelo
    list_display = ("first_name", "last_name", "username", "direccion", "celular")
    #Columnas con enlaces clickeables para entrar en el detalle
    list_display_links = ("first_name","last_name")
    #Campos por los que se puede buscar
    search_fields = ("first_name","last_name")
    #Orden por defecto
    ordering = ("first_name","last_name")