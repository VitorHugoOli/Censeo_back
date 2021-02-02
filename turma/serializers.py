from rest_framework import serializers

from curso.serializers import DisciplinaSerializer
from turma.models import Turma, DiasFixos, SugestaoTurma, TopicaTurma


class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turma
        fields = ['id', 'codigo', 'ano', 'semestre']


class TurmaDisciplinaSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer()

    class Meta:
        model = Turma
        fields = ['id', 'codigo', 'ano', 'semestre', 'disciplina']


class DiasFixosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiasFixos
        fields = ['id', 'dia', 'horario', 'sala']


class SugestaoTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugestaoTurma
        fields = ['id', 'sugestao', 'titulo', 'relevancia', 'data', 'topico']


class TopicaTurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicaTurma
        fields = ['id', 'topico']
