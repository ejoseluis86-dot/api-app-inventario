from rest_framework.permissions import BasePermission

from rest_framework.permissions import BasePermission

class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        
        # Obtenemos el rol y lo normalizamos
        rol = str(getattr(request.user, 'rol', '')).strip().upper()
        
        # Aceptamos tanto el código 'ADMIN' como la palabra 'ADMINISTRADOR'
        return rol in ['ADMIN', 'ADMINISTRADOR']

class EsAdminOEmpleado(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
            
        rol = str(getattr(request.user, 'rol', '')).strip().upper()
        
        # Aceptamos los códigos y las palabras completas
        return rol in ['ADMIN', 'ADMINISTRADOR', 'EMPL', 'EMPLEADO']