from django.db import models
from kiosco.models import Tarjeta
from productos.models import Producto

# Create your models here.
class Transaccion(models.Model):
    CONCEPTOS = (
        ("CARGA","Carga"),
        ("COMPRA","Compra"),
    )
    fecha = models.DateTimeField(auto_now_add=True)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.CASCADE, null=False)
    concepto = models.CharField(choices=CONCEPTOS, max_length=30, null=False)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    detalle = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f"{self.concepto} de $ {self.monto}"