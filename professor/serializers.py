from rest_framework import serializers

from professor.models import Professor


class ProfessorSerializer(serializers.HyperlinkedModelSerializer):
    user_u = serializers.PrimaryKeyRelatedField(source="user", read_only=True)

    class Meta:
        model = Professor
        fields = ['id', 'lattes', 'user_u']
