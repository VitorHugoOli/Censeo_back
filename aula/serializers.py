from rest_framework import serializers

from aula.models import Aula
from turma.serializers import TurmaSerializer


class SmallAulaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='idaula')
    turma = TurmaSerializer(source='turma_idturma')

    class Meta:
        model = Aula
        fields = ["id", "dia_horario", 'sala', 'turma']


class AulaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='idaula')
    horario = serializers.DateTimeField(source="dia_horario")
    turma = TurmaSerializer(source='turma_idturma')

    class Meta:
        model = Aula
        fields = ["id", "horario", 'sala', 'tipo_aula', 'tema', 'descricao', 'link_documento', 'turma']
