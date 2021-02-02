from rest_framework import serializers

from faculdade_sugestao.models import TopicoFaculdade, SugestaoFaculdade


class SugestaoFaculdadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SugestaoFaculdade
        fields = ['id', 'sugestao', 'titulo', 'relevancia', 'data']


class TopicoFaculdadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopicoFaculdade
        fields = ['id', 'topico']
