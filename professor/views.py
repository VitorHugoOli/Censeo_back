# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from curso.models import Curso, Disciplina
from professor.models import Professor
from professor.serializers import ProfessorSerializer
from turma.models import Turma, ProfessorHasTurma
from user.models import User


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggestions_categories(request):
    prof = Professor.objects.get(user=request.user)
    context: dict = {'categorias': {}}

    try:
        curso = Curso.objects.get(professor_coordenador=prof)
        context['categorias'][curso.codigo] = [
            {'id': curso.id, 'sigla': curso.codigo, 'nome': curso.nome, 'tipo': 'curso'}]
    except ObjectDoesNotExist as ex:
        pass

    prof_turma = ProfessorHasTurma.objects.filter(professor=prof)
    for i in prof_turma:
        turma = i.turma
        disp = Disciplina.objects.get(id=turma.disciplina.id)
        if context['categorias'].__contains__(disp.codigo):
            context['categorias'][disp.codigo].append(
                {'id': turma.id, 'sigla': disp.sigla, 'nome': disp.nome, 'codigo': turma.codigo, 'tipo': 'materia'})
        else:
            context['categorias'][disp.codigo] = [
                {'id': turma.id, 'sigla': disp.sigla, 'nome': disp.nome, 'codigo': turma.codigo, 'tipo': 'materia'}]

    return Response({'status': True, **context})
