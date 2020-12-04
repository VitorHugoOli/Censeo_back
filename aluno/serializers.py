from rest_framework import serializers

from aluno.models import Aluno, TopicoSugestaoCurso, SugestaoCurso
from user.serializers import UserSerializerWithoutToken


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    user_u = UserSerializerWithoutToken(source='user')

    class Meta:
        model = Aluno
        fields = ['id', 'xp', 'curso', 'user_u']


class TopicoSugestaoCursoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = TopicoSugestaoCurso
        fields = ['id', 'topico']


class SugestaoCursoSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SugestaoCurso
        fields = ['id', 'sugestao', 'titulo', 'relevancia','data']
