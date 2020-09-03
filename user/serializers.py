from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.utils.serializer_helpers import ReturnDict

from user.models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    type = serializers.CharField(source='tipo_user')

    @property
    def data(self):
        ret = super().data
        token = Token.objects.get(user=self.instance).key
        ret.update({"token": token})
        return ReturnDict(ret, serializer=self)

    class Meta:
        model = User
        fields = ['id', 'nome', 'matricula', 'username', 'email', 'first_time', 'type', 'token']


class UserSerializerWithoutToken(serializers.HyperlinkedModelSerializer):
    type = serializers.CharField(source='tipo_user')

    class Meta:
        model = User
        fields = ['id', 'nome', 'matricula', 'username', 'email', 'first_time', 'type']
