from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from aluno.models import Aluno, TopicoSugestaoCurso, SugestaoCurso
from avatar.models import AvatarHasAluno
from user.serializers import UserSerializerWithoutToken
from avatar.serializers import *


class AvatarField(serializers.RelatedField):
    def to_representation(self, value):
        avatar = AvatarHasAluno.objects.get(aluno=self.instance, is_active=True)
        return AvatarHasAlunoSerializer(avatar)


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    user_u = UserSerializerWithoutToken(source='user')

    @property
    def data(self):
        ret = super().data
        try:
            perfilPhoto = AvatarHasAluno.objects.get(aluno=self.instance, is_active=True).avatar.url
        except AvatarHasAluno.DoesNotExist:
            perfilPhoto = None
        ret.update({"perfilPhoto": perfilPhoto})
        return ReturnDict(ret, serializer=self)

    class Meta:
        model = Aluno
        fields = ['id', 'xp', 'curso', 'user_u']


class TopicoSugestaoCursoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TopicoSugestaoCurso
        fields = ['id', 'topico']


class SugestaoCursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugestaoCurso
        fields = ['id', 'sugestao', 'titulo', 'relevancia', 'data', 'topico']
