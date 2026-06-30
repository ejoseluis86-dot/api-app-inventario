from django.db import models
#clase 1
class Insumo(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=100)
    stock = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre
    
#clase 2
class ConsumoRealInsumo(models.Model):
    cantidadReal = models.PositiveIntegerField()
    detallePedido = models.ForeignKey(
        'DetallePedido',
        on_delete=models.PROTECT,
    )
    insumo= models.ForeignKey(
        'Insumo',
        on_delete=models.PROTECT,
    )

#clase 3
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.CharField(max_length=100)
    activo = models.BooleanField(default=True)
    def __str__(self):
        return self.nombre

#clase 4
class DetallePedido (models.Model):
    cantidad = models.PositiveIntegerField()
    precioUnitario= models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.PositiveIntegerField()
    pedido = models.ForeignKey(
        'Pedido',
        on_delete= models.CASCADE,
    )
    producto = models.ForeignKey(
        'Producto',
        on_delete=models.PROTECT,
    )
    
#clase 5
class Pedido(models.Model):
    fecha = models.DateField()
    cliente= models.CharField(max_length=100)
    usuario = models.ForeignKey(
        'Usuario',
        on_delete=models.PROTECT
    )
    terminado= models.BooleanField(default=False)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)


#clasea 6 
class DetalleReceta(models.Model):
    cantidadTeorica= models.PositiveIntegerField()
    insumo = models.ForeignKey(
        'Insumo',
        on_delete=models.PROTECT
    )
    producto= models.ForeignKey(
        'Producto',
        on_delete=models.CASCADE
    )


#clase 7
from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):

    ROLES = [
        ('ADMIN', 'Administrador'),
        ('EMPL', 'Empleado'),
    ]

    rol = models.CharField(
        max_length=5,
        choices=ROLES,
        default='EMPL'
    )
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.rol = 'ADMIN'
        super().save(*args, **kwargs)    
