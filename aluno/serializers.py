from rest_framework import serializers

from aluno.models import Aluno


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(source="user_iduser", read_only=True)
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    id = serializers.IntegerField(source='idaluno')

    class Meta:
        model = Aluno
        fields = ['id', 'xp', 'curso', 'user_id']
