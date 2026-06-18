from django.contrib import admin
from .models import Insumo,ConsumoRealInsumo,Producto,DetallePedido,Pedido, DetalleReceta,Usuario

# Register your models here.

admin.site.register(Insumo)
admin.site.register(ConsumoRealInsumo)
admin.site.register(Producto)
admin.site.register(DetallePedido)
admin.site.register(DetalleReceta)
admin.site.register(Pedido)
admin.site.register(Usuario)
