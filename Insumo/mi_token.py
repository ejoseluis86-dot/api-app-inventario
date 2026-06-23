from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class MiToken(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        data['id'] = user.id
        data['username'] = user.username
        data['nombre'] = user.first_name
        data['apellido'] = user.last_name
        data['permiso'] = user.rol

        return data