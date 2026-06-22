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

#1 Lista Get
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def listaInsumos(request):
    insumos = list(Insumo.objects.values())
    return JsonResponse(insumos, safe=False)

#2 modificar insumo
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
    
#3 crear insumo
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
    

#4 gregar un producto con detalles
@api_view(['POST'])
@permission_classes([EsAdminOEmpleado])
@csrf_exempt
def crearProducto(request):
    try:
        print('si entro')
        # Convertir el JSON recibido en el body a un diccionario Python
        data = json.loads(request.body)

        # Crear el producto en la base de datos
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
#5 lista de productoLite
@api_view(['GET'])
@permission_classes([EsAdminOEmpleado])
def listaProductos(request):
    
    productos = list(
        Producto.objects.values(
            'id',
            'nombre',
            'precio'
        )
    )

    return JsonResponse(productos, safe=False)

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
    # Convertir el JSON recibido en el body a un diccionario Python
    data = json.loads(request.body)

    # Crear el pedido en la base de datos
    pedido = Pedido.objects.create(
        fecha=data['fecha'],
        cliente=data['cliente'],
        usuario_id=data['usuario']
    )

    # Recorrer la lista de detalles enviada en el JSON esto talvez se modifique
    for detalle in data['detalles']:
        print(detalle)
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
        producto_id = id_producto
    ).values()

    return JsonResponse(list(detalles), safe=False)

#13 cambiar estado del pedido a true
@api_view(['PUT'])
@permission_classes([EsAdminOEmpleado])
def cambiarEstadoPedido(request, id_pedido):
    pedido = Pedido.objects.get(id=id_pedido)
    pedido.terminado= True
    pedido.save


#esto es para el token personalizado
class MiTokenObtainPairView(TokenObtainPairView):
    serializer_class = MiToken

#14crear usuario
@api_view(['POST'])
@permission_classes([EsAdmin])
def crearUsuario(request):
 
 try:

    data = request.data
    
    username = data.get('username')
    password = data.get('password')
    rol = data.get('rol', 'EMPL')
    if not username or not password:
        return JsonResponse({'mensaje': 'username y password son obligatorios'}, status=400)
    user = Usuario.objects.create_user(
        username=username,
        password=password,
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