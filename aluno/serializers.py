from rest_framework import serializers

from aluno.models import Aluno
from user.serializers import UserSerializerWithoutToken


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    user = UserSerializerWithoutToken(read_only=True)
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)

    class Meta:
        model = Aluno
        fields = ['id', 'xp', 'curso', 'user']
