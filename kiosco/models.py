from django.db import models
from django.core.validators import MinValueValidator

class Cliente(models.Model):
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

# class Producto(models.Model):
#     nombre = models.CharField(max_length=50, null=False)
#     marca = models.CharField(max_length=30, null=False)
#     categoria = models.CharField(max_length=30, null=False)
#     precio = models.DecimalField(max_digits=8, decimal_places=2)
#     stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
#     codigo_de_barras = models.CharField(max_length=13, null=False)

#     def __str__(self):
#         return f"{self.nombre} {self.marca}/ Precio: $ {self.precio}/ Stock: {self.stock}"

