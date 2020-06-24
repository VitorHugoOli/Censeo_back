from rest_framework import serializers

from aluno.models import Aluno


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    id = serializers.IntegerField(source='idaluno')

    class Meta:
        model = Aluno
        fields = ['id', 'nome', 'matricula', 'username', 'email', 'xp', 'first_time', 'curso']
