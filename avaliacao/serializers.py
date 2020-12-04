from rest_framework import serializers

from avaliacao.models import Avaliacao, Pergunta, Caracteristica, Resposta


class AvaliacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avaliacao
        fields = ['id', 'aula', 'aluno']


class CaracteristicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Caracteristica
        fields = ['qualificacao']


class PerguntaSerializer(serializers.ModelSerializer):
    caracteristica = CaracteristicaSerializer()

    class Meta:
        model = Pergunta
        fields = ['id', 'questao', 'tipo_questao', 'tipo_aula', 'caracteristica']


class RespostaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resposta
        fields = ['id', 'resposta_aberta', 'resposta_qualificativa', 'resposta_binario', 'tipo_resposta']
