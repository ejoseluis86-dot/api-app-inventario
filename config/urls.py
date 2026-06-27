from Insumo import views
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from Insumo.views import MiTokenObtainPairView




urlpatterns = [
    path('admin/', admin.site.urls),
    path('insumos/', views.listaInsumos),
    path('insumos/modificar/<int:id_insumo>/', views.modificarInsumo),
    path('insumos/insumo', views.crearInsumo),
    path('insumos/eliminar/<int:id_insumo>/',  views.eliminarInsumo),
    path('productos/crear/', views.crearProducto),
    path('productos/modificar/<int:id_producto>/', views.modificarProducto),
    path('productos/eliminar/<int:id_producto>/', views.eliminarProducto),
    path('productos/', views.listaProductos),
    path('productos/completos/', views.listaProductosCompletos),
    path('productos/<int:id_producto>/', views.detalleProducto,
),
    path('consumos/crear/', views.crearConsumo),
    path('pedidos/crear/', views.crearPedido),
    path('pedidos/sin-terminar/', views.pedidosSinTerminar),
    path('pedidos/terminados/', views.pedidosTerminados),
    path('pedidos/<int:id_detalle>/consumos/', views.consumosDelDetalle),
    path('pedidos/<int:id_pedido>/detalles/', views.detallesPedido),
    path('productos/<int:id_producto>/detalles-receta/', views.detallesReceta),
    #esto es para los usuarios
    path('login/',MiTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view(),name= 'token_refresh'),
    path('usuarios/crear/', views.crearUsuario),
    path('usuarios/miPerfil/', views.miPerfil),
    path('usuarios/modificarMiPerfil/', views.modificarMiPerfil),

]
