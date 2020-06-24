from rest_framework import serializers

from professor.models import Professor


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.IntegerField(source='idprofessor')

    class Meta:
        model = Professor
        fields = ['id','nome','matricula', 'username', 'email','lattes','frist_time']