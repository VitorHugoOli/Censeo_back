from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from Utils.Except import generic_except
from curso.models import Curso
from curso.serializers import CursoSerializer
from faculdade.models import Faculdade
from professor.models import Professor


class CursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Curso.objects.all()
    serializer_class = CursoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            try:
                prof = Professor.objects.get(id=data.get('prof'))
            except ObjectDoesNotExist as ex:
                prof = None
            try:
                facu = Faculdade.objects.get(id=data.get('facu'))
            except ObjectDoesNotExist as ex:
                facu = None

            curso = Curso(
                nome=data['name'],
                codigo=data['codigo'],
                faculdade=facu,
                professor_coordenador=prof,
            )
            curso.save()
            serializer_context = {
                'request': request,
            }

            return Response({'status': True, 'curso': CursoSerializer(curso, context=serializer_context).data})
        except IntegrityError as ex:
            return Response({'status': False, 'error': "Algum campo está faltando.", 'except': ex.args})
        except Exception as ex:
            return generic_except(ex)
