from rest_framework import serializers

from curso.models import Curso, Disciplina


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    prof = serializers.PrimaryKeyRelatedField(source="professor_cordenador", read_only=True)

    class Meta:
        model = Curso
        fields = ['idcurso', 'nome', 'codigo', 'prof']


class DisciplinaSerializer(serializers.HyperlinkedModelSerializer):
    curso = serializers.PrimaryKeyRelatedField(source="curso_idcurso", read_only=True)
    id = serializers.IntegerField(source='iddisciplina')

    class Meta:
        model = Disciplina
        fields = ['id', 'codigo', 'nome', 'sigla', 'curso']
