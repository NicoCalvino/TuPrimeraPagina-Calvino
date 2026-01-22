from django.contrib import admin
from transacciones.models import *

@admin.register(Transaccion)
class TransaccionAdmin(admin.ModelAdmin):
    list_display = ("concepto", "fecha", "tarjeta", "monto")
    list_display_links = ("concepto","tarjeta")
    search_fields = ("concepto","tarjeta")
    ordering = ("fecha", )
    readonly_fields = ("fecha","concepto")

@admin.register(SolicitudCarga)
class SolicitudCargaAdmin(admin.ModelAdmin):
    list_display = ("code", "usuario", "fecha", "fecha_ultima_modificacion", "monto","estado")
    list_display_links = ("code","usuario")
    search_fields = ("code","usuario")
    ordering = ("fecha_ultima_modificacion", )
    readonly_fields = ("fecha_ultima_modificacion","fecha","usuario","code")

@admin.register(DetalleCarga)
class DetalleCargaAdmin(admin.ModelAdmin):
    list_display = ("solicitud", "tarjeta", "monto")
    list_display_links = ("solicitud",)
    search_fields = ("solicitud","tarjeta")
    ordering = ("solicitud", )
    readonly_fields = ("solicitud","tarjeta")