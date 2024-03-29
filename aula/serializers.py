from rest_framework import serializers

from aula.models import Aula
from turma.serializers import TurmaSerializer, TurmaDisciplinaSerializer


class SmallAulaSerializer(serializers.HyperlinkedModelSerializer):
    turma = TurmaSerializer()

    class Meta:
        model = Aula
        fields = ["id", "dia_horario", 'sala', 'turma', ]


class AulaSerializer(serializers.HyperlinkedModelSerializer):
    horario = serializers.DateTimeField(source="dia_horario")
    turma = TurmaDisciplinaSerializer()

    class Meta:
        model = Aula
        fields = ["id", "horario", 'sala', 'tipo_aula', 'tema', 'descricao', 'link_documento', 'is_assincrona',
                  'end_time', 'turma']
