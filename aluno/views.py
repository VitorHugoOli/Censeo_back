# Create your views here.
from rest_framework import viewsets, permissions

from aluno.models import Aluno
from aluno.serializers import AlunoSerializer


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]



