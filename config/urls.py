from Insumo import views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('insumos/', views.listaInsumos),
    path('insumos/modificar/<int:id_insumo>/', views.modificarInsumo),
    path('insumos/insumo', views.crearInsumo),
    path('productos/crear/', views.crearProducto),
    path('productos/', views.listaProductos),
    path('consumos/crear/', views.crearConsumo),
    path('pedidos/crear/', views.crearPedido),
    path('pedidos/sin-terminar/', views.pedidosSinTerminar),
    path('pedidos/terminados/', views.pedidosTerminados),
    path('pedidos/<int:id_detalle>/consumos/', views.consumosDelDetalle),
    path('pedidos/<int:id_pedido>/detalles/', views.detallesPedido),
    path('productos/<int:id_producto>/detalles-receta/', views.detallesReceta),
]
