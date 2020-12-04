from rest_framework import serializers

from curso.models import Curso, Disciplina


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    prof = serializers.PrimaryKeyRelatedField(source="professor_coordenador", read_only=True)

    class Meta:
        model = Curso
        fields = ['id', 'nome', 'codigo', 'prof']


class DisciplinaSerializer(serializers.ModelSerializer):
    # curso = serializers.PrimaryKeyRelatedField(source="curso", read_only=True)

    class Meta:
        model = Disciplina
        fields = ['id', 'codigo', 'nome', 'sigla', 'curso']
