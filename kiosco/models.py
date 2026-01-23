from django.db import models
from django.core.validators import MinValueValidator, MinLengthValidator
from django.conf import settings

class Cliente(models.Model):
    CURSOS = (
        ("SALA DE 5","Sala de 5"),
        ("1° GRADO","1° Grado"),
        ("2° GRADO","2° Grado"),
        ("3° GRADO","3° Grado"),
        ("4° GRADO","4° Grado"),
        ("5° GRADO","5° Grado"),
        ("6° GRADO","6° Grado"),
        ("1 AÑO","1 Año"),
        ("2 AÑO","2 Año"),
        ("3 AÑO","3 Año"),
        ("4 AÑO","4 Año"),
        ("5 AÑO","5 Año"),
        ("6 AÑO","6 Año"),
    )
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='clientes', null=False)
    nombre = models.CharField(max_length=50, null=False)
    apellido = models.CharField(max_length=50, null=False)
    curso = models.CharField(choices=CURSOS, max_length=10, null=False)

    @property
    def saldo_total(self):
        total = sum(tarjeta.saldo for tarjeta in self.tarjeta_set.all())
        return total

    def ultimos_movimientos(self):
        movimientos = []
        
        for tarjeta in self.tarjeta_set.all():
            movimientos .extend(tarjeta.transaccion_set.all())
        
        movimientos.sort(key=lambda x: x.fecha, reverse=True)
        
        return movimientos[:10]

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.curso}"

class Tarjeta(models.Model):
    codigo = models.CharField(max_length=15, unique=True, null=False, validators=[MinLengthValidator(15)])
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0, validators=[MinValueValidator(-2000)])
    habilitada = models.BooleanField(default=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, null=True)

    fecha_activacion = models.DateTimeField(auto_now_add=True)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo}"
