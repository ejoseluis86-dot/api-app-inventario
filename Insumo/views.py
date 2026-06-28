import json
import traceback
#esto es para el error de seguridad 
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
#esto es para modificar el json del token 
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from Insumo.mi_token import MiToken
#esto es para las views
from .models import ConsumoRealInsumo, DetallePedido, DetalleReceta, Insumo, Pedido, Producto, Usuario
#esto es para los permisos de los endpoints

from .permisos import EsAdminOEmpleado
from .permisos import EsAdmin

from django.contrib.auth import get_user_model

#1 Lista Get Insumos
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def listaInsumos(request):
    insumos = list(Insumo.objects.values())
    return JsonResponse(insumos, safe=False)

#---------------------
# Modificar insumo
#---------------------
@api_view(['PUT'])
@permission_classes([EsAdminOEmpleado])
def modificarInsumo(request, id_insumo):
    try:
        data = json.loads(request.body)
        insumo = Insumo.objects.get(id=id_insumo)

        insumo.nombre = data.get('nombre', insumo.nombre)
        insumo.categoria = data.get('categoria', insumo.categoria)
        insumo.stock = data.get('stock', insumo.stock)
        insumo.ubicacion = data.get('ubicacion', insumo.ubicacion)

        insumo.save()

        return JsonResponse({
            'mensaje': 'Insumo actualizado',
            'id': insumo.id
        })

    except Insumo.DoesNotExist:
        return JsonResponse({'error': 'No existe'}, status=404)

#-------------------------------------    
# Crear insumo
#-------------------------------------
@api_view(['POST'])
@permission_classes([EsAdmin])
@csrf_exempt
def crearInsumo(request):

    data = json.loads(request.body)
    insumo = Insumo.objects.create(
    nombre=data['nombre'],
    categoria=data['categoria'],
    stock=data['stock'],
    ubicacion=data['ubicacion']
    )
    
    return JsonResponse({
        "id": insumo.id,
        "nombre": insumo.nombre,
        "categoria": insumo.categoria,
        "stock": insumo.stock,
        "ubicacion":insumo.ubicacion
        }, status=200)

#-------------------------------------    
# Eliminar insumo
#-------------------------------------
@api_view(['DELETE'])
@permission_classes([EsAdmin])
def eliminarInsumo(request, id_insumo):
    try:
        insumo = Insumo.objects.get(id=id_insumo)
        insumo.delete()

        return JsonResponse({
            'mensaje': 'Insumo eliminado'
        })

    except Insumo.DoesNotExist:
        return JsonResponse(
            {'error': 'No existe'},
            status=404
        )
        
#-------------------------------------
# Verificar si un producto ya existe
#-------------------------------------        
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def existeProducto(request, nombre):
    existe = Producto.objects.filter(nombre__iexact=nombre).exists()

    return JsonResponse({
        "existe": existe
    })        
        
#-------------------------------------
# Agregar un producto con detalles
#-------------------------------------
@api_view(['POST'])
@permission_classes([EsAdmin])
@csrf_exempt
def crearProducto(request):
    try:
        print('si entro')
        # Convertir el JSON recibido en el body a un diccionario Python
        data = json.loads(request.body)

        # VALIDAR DUPLICADOS 
        if Producto.objects.filter(
            nombre__iexact=data['nombre'].strip()
        ).exists():
            return JsonResponse(
                {"error": "Ya existe un producto con ese nombre"},
                status=400
            )

        # SI NO EXISTE, CREAR EL PRODUCTO
        producto = Producto.objects.create(
            nombre=data['nombre'],
            precio=data['precio'],
            categoria=data['categoria']
        )

        # Recorrer la lista de detalles enviada en el JSON
        for detalle in data['detalles']:

            # Buscar el insumo por su id
            insumo = Insumo.objects.get(
                id=detalle['insumo_id']
            )

            # Crear un detalle de receta
            DetalleReceta.objects.create(
                # Relacionar con el producto recién creado
                producto=producto,

                # Relacionar con el insumo encontrado
                insumo=insumo,

                # Guardar la cantidad teórica
                cantidadTeorica=detalle['cantidad_teorica']
            )
        # Devolver respuesta de éxito
        return JsonResponse(
            {
                'id_producto': producto.id,
                'mensaje': 'Producto creado correctamente'
            },
            status=201
        )
    except Insumo.DoesNotExist:
        return JsonResponse({'error': 'Producto no encontrado'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)})
    

#---------------------
# Modificar producto
#----------------------
@api_view(['PUT'])
@permission_classes([EsAdmin])
def modificarProducto(request, id_producto):
    try:
        data = json.loads(request.body)
        producto = Producto.objects.get(id=id_producto)

        producto.nombre = data.get('nombre', producto.nombre)
        producto.precio = data.get('precio', producto.precio)
        producto.categoria = data.get('categoria', producto.categoria)

        producto.save()
        
        # eliminar receta vieja
        DetalleReceta.objects.filter(producto=producto).delete()

        # crear nueva receta
        for detalle in data.get('detalles', []):
            insumo = Insumo.objects.get(id=detalle['insumo_id'])

            DetalleReceta.objects.create(
                producto=producto,
                insumo=insumo,
                cantidadTeorica=detalle['cantidad_teorica']
            )

        return JsonResponse({
            "mensaje": "Producto actualizado",
            "id": producto.id
        })

    except Producto.DoesNotExist:
        return JsonResponse({"error": "No existe"}, status=404)

#---------------------
# "ELIMINAR" producto - solo pasa de activo a inactivo 
#---------------------
@api_view(['DELETE'])
@permission_classes([EsAdmin])
def eliminarProducto(request, id_producto):
    try:
        producto = Producto.objects.get(id=id_producto)

        producto.activo = False
        producto.save()

        return JsonResponse({
            "mensaje": "Producto desactivado"
        })

    except Producto.DoesNotExist:
        return JsonResponse(
            {"error": "No existe"},
            status=404,
        )

#-----------------------------------
# Lista de productos para empleados
#-----------------------------------
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def listaProductos(request):

    productos = Producto.objects.filter(activo=True)

    data = []

    for producto in productos:
        detalles = DetalleReceta.objects.filter(producto=producto)

        data.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria,
            "detalles": [
                {
                    "id": d.id,
                    "insumoId": d.insumo.id,
                    "nombreInsumo": d.insumo.nombre,
                    "cantidadTeorica": d.cantidadTeorica,
                }
                for d in detalles
            ]
        })
    return JsonResponse(data, safe=False)

#---------------------
# nueva lista de productos completos - oculta los inactivos para empleados
#----------------------
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def listaProductosCompletos(request):

    productos = Producto.objects.filter(activo=True)

    data = []

    for producto in productos:

        data.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria,
        })

    return JsonResponse(data, safe=False)



#-----------------------------------------
# Lista de todos los productos para admin
#-----------------------------------------
@api_view(['GET'])
@permission_classes([EsAdmin])
def listaProductosAdmin(request):

    productos = Producto.objects.all()

    data = []

    for producto in productos:
        detalles = DetalleReceta.objects.filter(producto=producto)

        data.append({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria,
            "activo": producto.activo,  # 👈 CLAVE
            "detalles": [
                {
                    "id": d.id,
                    "insumoId": d.insumo.id,
                    "nombreInsumo": d.insumo.nombre,
                    "cantidadTeorica": d.cantidadTeorica,
                }
                for d in detalles
            ]
        })

    return JsonResponse(data, safe=False)







#6 crear un consumo real
@api_view(['POST'])
@permission_classes([EsAdminOEmpleado])
@csrf_exempt
def crearConsumo(request):
    try:
        data = json.loads(request.body)
        detalle= DetallePedido.objects.get(pk=data['detallePedido_id'])
        print(detalle)
        insumo= Insumo.objects.get(pk=data['insumo_id'])
        print(insumo)
        consumo = ConsumoRealInsumo.objects.create(
            cantidadReal=data['cantidadReal'],
            detallePedido= detalle,
            insumo=insumo
        )

        return JsonResponse({
            'id': consumo.id,
            'id_detalle': consumo.detallePedido.pk
        }, status=201)

    except Exception as e:
        return JsonResponse({
            'error el detalle o el insumo no existe': str(e)
        }, status=500)

#7 crear pedido
@api_view(['POST'])
@permission_classes([EsAdminOEmpleado])
@csrf_exempt
def crearPedido(request):
    from datetime import datetime

    # Convertir el JSON recibido en el body a un diccionario Python
    data = json.loads(request.body)
    #estoy parseando la fecha del json de formato ISO a data
    fecha = datetime.fromisoformat(data['fecha'])
    # Crear el pedido en la base de datos
    pedido = Pedido.objects.create(
        fecha= fecha,
        cliente=data['cliente'],
        usuario_id=data['usuario']
    )

    # Recorrer la lista de detalles enviada en el JSON esto talvez se modifique
    for detalle in data['detalles']:
        # Crear un detalle de receta
        DetallePedido.objects.create(
            cantidad = detalle['cantidad'],
            precioUnitario =detalle['precio'],
            descuento = detalle['descuento'],
            pedido = pedido ,
            producto_id = detalle['producto_id'],
        )
    # Devolver respuesta de éxito
    return JsonResponse(
        {
            'id_pedido': pedido.id,
            'mensaje': 'Pedido creado correctamente'
        },
        status=201
    )


#8 lista de pedidosLite sin terminar cuyo atributo bool sea false
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def pedidosSinTerminar(request):
    pedidos = Pedido.objects.filter(terminado=False)

    data = []

    for pedido in pedidos:
        data.append({
            'id': pedido.id,
            'cliente': pedido.cliente,
            'fecha': pedido.fecha,
        })

    return JsonResponse(data, safe=False)

#9 lista de pedidosLite terminados cuyo atributo bool sea true
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def pedidosTerminados(request):
    pedidos = Pedido.objects.filter(terminado=True)

    data = []

    for pedido in pedidos:
        data.append({
            'id': pedido.id,
            'cliente': pedido.cliente,
            'fecha': pedido.fecha,
        })

    return JsonResponse(data, safe=False)

#10 lista de consumos Reales por id_pedido
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def consumosDelDetalle(request, id_detalle):
    consumos = ConsumoRealInsumo.objects.filter(
        detallePedido_id=id_detalle
    )

    data = []

    for consumo in consumos:
        data.append({
            'id': consumo.id,
            'cantidadReal': consumo.cantidadReal,
            'insumo_id': consumo.insumo_id
        })

    return JsonResponse(data, safe=False)

#11 lista de DetallePedido por id_pedido
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def  detallesPedido(request, id_pedido):
    detalles = DetallePedido.objects.filter(
        pedido_id=id_pedido
    ).values()

    return JsonResponse(list(detalles), safe=False)

#12 lista de DetalleReceta por id_producto
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def detallesReceta(request, id_producto):

    detalles = DetalleReceta.objects.filter(
        producto_id=id_producto
    )

    data = []

    for detalle in detalles:
        data.append({
            "insumo": detalle.insumo.nombre,
            "cantidadTeorica": detalle.cantidadTeorica,
        })

    return JsonResponse(data, safe=False)

#13 cambiar estado del pedido a true
@api_view(['PUT'])
@permission_classes([EsAdminOEmpleado])
def cambiarEstadoPedido(request, id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    pedido.terminado= True
    pedido.save()

#esto es para el token personalizado
class MiTokenObtainPairView(TokenObtainPairView):
    serializer_class = MiToken

#14 Crear usuario
@api_view(['POST'])
@permission_classes([EsAdmin])
def crearUsuario(request):
 
 try:

    data = request.data
    
    username = data.get('username')
    password = data.get('password')
    rol = data.get('rol', 'EMPL')
    nombre = data.get('nombre', '')
    apellido = data.get('apellido', '')
    
    if not username or not password:
        return JsonResponse({'mensaje': 'username y password son obligatorios'}, status=400)
    user = Usuario.objects.create_user(
        username=username,
        password=password,
        first_name=nombre,
        last_name=apellido,
        rol=rol
    )
    return JsonResponse({
        'id': user.id,
        'username': user.username,
        'rol': user.rol
    }, status=201)
 except Exception as e:
        print(traceback.format_exc())
        return JsonResponse({'error el usuario ya existe'}, status=500)

#15 Perfil del usuario    
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def miPerfil(request):

    print("ENTRÓ A miPerfil")
    print("USER:", request.user)
    print("AUTH:", request.user.is_authenticated)

    usuario = request.user

    return JsonResponse({
        'id': usuario.id,
        'username': usuario.username,
        'nombre': usuario.first_name,
        'apellido': usuario.last_name,
        'rol': usuario.rol,
    })

#16 Editar perfil del usuario
@api_view(['PUT'])
@permission_classes([EsAdminOEmpleado])
def modificarMiPerfil(request):

    usuario = request.user
    data = json.loads(request.body)

    usuario.first_name = data.get('nombre', usuario.first_name)
    usuario.last_name = data.get('apellido', usuario.last_name)

    # opcional: cambiar username
    if data.get('username'):
        usuario.username = data.get('username')

    usuario.save()

    return JsonResponse({
        'mensaje': 'Perfil actualizado correctamente'
    })


#17 OBTENER PRODUCTO CON SU RECETA
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def detalleProducto(request, id_producto):

    try:
        producto = Producto.objects.get(id=id_producto)

        detalles = DetalleReceta.objects.filter(producto=producto)

        lista_detalles = []

        for detalle in detalles:
            lista_detalles.append({
                "id": detalle.id,
                "cantidad_teorica": detalle.cantidadTeorica,
                "insumo_id": detalle.insumo.id,
                "producto_id": producto.id,
                "nombre_insumo": detalle.insumo.nombre,
            })

        return JsonResponse({
            "id": producto.id,
            "nombre": producto.nombre,
            "precio": producto.precio,
            "categoria": producto.categoria,
            "detalles": lista_detalles,
        })

    except Producto.DoesNotExist:
        return JsonResponse(
            {"error": "No existe"},
            status=404,
        )   
    
        