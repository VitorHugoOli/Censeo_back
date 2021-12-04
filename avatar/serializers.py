from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnDict

from aluno.models import Aluno, TopicoSugestaoCurso, SugestaoCurso
from avatar.models import *
from user.serializers import UserSerializerWithoutToken


class AvatarSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'url']


class AvatarHasAlunoSerializer(serializers.ModelSerializer):
    avatar_u = AvatarSerializer(source='avatar')

    class Meta:
        model = AvatarHasAluno
        fields = ['avatar_u', 'is_active']
