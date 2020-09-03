from rest_framework import serializers

from turma.models import Turma, DiasFixos, SugestaoTurma, TopicaTurma


class TurmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'codigo', 'ano', 'semestre']


class DiasFixosSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DiasFixos
        fields = ['id', 'dia', 'horario', 'sala']


class SugestaoTurmaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SugestaoTurma
        fields = ['id', 'sugestao', 'titulo', 'relevancia']


class TopicaTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicaTurma
        fields = ['id', 'topico']
