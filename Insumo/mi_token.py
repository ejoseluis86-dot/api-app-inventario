from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MiToken(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user=self.user
        data['id'] = user.id
        data['nombre'] = user.username
        data['permiso'] = user.rol
        return data