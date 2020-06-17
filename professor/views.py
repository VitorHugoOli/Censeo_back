from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from professor.models import Professor
from professor.serializers import ProfessorSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response({'status':True})