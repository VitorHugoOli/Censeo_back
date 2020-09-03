from rest_framework import serializers

from aula.models import Aula
from turma.serializers import TurmaSerializer


class SmallAulaSerializer(serializers.HyperlinkedModelSerializer):
    turma = TurmaSerializer()

    class Meta:
        model = Aula
        fields = ["id", "dia_horario", 'sala', 'turma']


class AulaSerializer(serializers.HyperlinkedModelSerializer):
    horario = serializers.DateTimeField(source="dia_horario")
    turma = TurmaSerializer()

    class Meta:
        model = Aula
        fields = ["id", "horario", 'sala', 'tipo_aula', 'tema', 'descricao', 'link_documento', 'turma']
