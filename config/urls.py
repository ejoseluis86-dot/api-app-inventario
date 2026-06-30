from Insumo import views
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from Insumo.views import MiTokenObtainPairView
from Insumo.views import cambiarEstadoPedido




urlpatterns = [
    path('admin/', admin.site.urls),
    path('insumos/', views.listaInsumos),
    path('insumos/modificar/<int:id_insumo>/', views.modificarInsumo),
    path('insumos/insumo', views.crearInsumo),
    path('insumos/eliminar/<int:id_insumo>/',  views.eliminarInsumo),
    path('insumos/toggle/<int:id_insumo>/', views.toggleInsumo),
    path('productos/existe/<str:nombre>/', views.existeProducto),
    path('productos/crear/', views.crearProducto),
    path('productos/modificar/<int:id_producto>/', views.modificarProducto),
    path('productos/eliminar/<int:id_producto>/', views.eliminarProducto),
    path('productos/', views.listaProductos),
    path('productos/completos/', views.listaProductosCompletos),
    path('productos/admin/', views.listaProductosAdmin),
    path('productos/toggle/<int:id_producto>/', views.toggleProducto),
    path('productos/<int:id_producto>/', views.detalleProducto,),
    path('consumos/crear/', views.crearConsumo),
    path('pedidos/crear/', views.crearPedido),
    path('pedidos/sin-terminar/', views.pedidosSinTerminar),
    path('pedidos/terminados/', views.pedidosTerminados),
    path('finalizar_pedido/<int:id_pedido>/', cambiarEstadoPedido, name='finalizar_pedido'),
    path('pedidos/<int:id_detalle>/consumos/', views.consumosDelDetalle),
    path('pedidos/<int:id_pedido>/detalles/', views.detallesPedido),
    path('productos/<int:id_producto>/detalles-receta/', views.detallesReceta),
    #esto es para los usuarios
    path('login/',MiTokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view(),name= 'token_refresh'),
    path('usuarios/crear/', views.crearUsuario),
    path('usuarios/miPerfil/', views.miPerfil),
    path('usuarios/modificarMiPerfil/', views.modificarMiPerfil),
    # Rutas para el Panel de Gestión de Usuarios
    path('usuarios/admin/listado/', views.listaUsuariosAdmin, name='lista-usuarios-admin'),
    path('usuarios/admin/toggle/<int:id_usuario>/', views.toggleUsuario, name='toggle-usuario'),
    path('usuarios/admin/editar/<int:id_usuario>/', views.editar_usuario_admin, name='editar-usuario-admin'),

]
