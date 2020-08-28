from rest_framework import serializers

from aluno.models import Aluno
from user.serializers import UserSerializerWithoutToken


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializerWithoutToken(source="user_iduser", read_only=True)
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    id = serializers.IntegerField(source='idaluno')

    class Meta:
        model = Aluno
        fields = ['id', 'xp', 'curso', 'user']
