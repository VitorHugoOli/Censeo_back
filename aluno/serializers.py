from rest_framework import serializers

from professor.models import Professor


class AlunoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome','matricula', 'username', 'email','xp']