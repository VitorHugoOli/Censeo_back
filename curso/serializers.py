from rest_framework import serializers

from curso.models import Curso


class CursoSerializer(serializers.HyperlinkedModelSerializer):
    prof = serializers.PrimaryKeyRelatedField(source="professor_cordenador", read_only=True)

    class Meta:
        model = Curso
        fields = ['idcurso', 'nome', 'codigo', 'prof']
