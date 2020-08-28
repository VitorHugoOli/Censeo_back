from rest_framework import serializers

from turma.models import Turma, DiasFixos, SugestaoTurma


class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='idturma')

    class Meta:
        model = Turma
        fields = ['id', 'codigo', 'ano', 'semestre']


class DiasFixosSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='iddias_fixos')

    class Meta:
        model = DiasFixos
        fields = ['id', 'dia', 'horario', 'sala']


class SugestaoTurmaSerializer(serializers.HyperlinkedModelSerializer):
    # id = serializers.IntegerField(source='idsugestao_turma')

    class Meta:
        model = SugestaoTurma
        fields = ['idsugestao_turma', 'sugestao', 'titulo', 'relevancia']
