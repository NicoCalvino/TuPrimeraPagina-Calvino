from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings

class Cliente(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clientes', null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    curso = models.CharField(max_length=10, null=False)

    def __str__(self):
        return f"Cliente: {self.nombre} {self.apellido}"

class Tarjeta(models.Model):
    codigo = models.CharField(max_length=15, null=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(-2000)])
    alumna = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)
    fecha_activacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tarjeta: {self.codigo} / Saldo: $ {self.saldo}"
