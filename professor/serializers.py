from rest_framework import serializers

from professor.models import Professor
from user.serializers import UserSerializer


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(source="user_iduser",read_only=True)
    id = serializers.IntegerField(source='idprofessor')

    class Meta:
        model = Professor
        fields = ['id', 'lattes','user']
