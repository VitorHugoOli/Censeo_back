from rest_framework import serializers

from professor.models import Professor


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Professor
        fields = ['nome', 'username', 'email']