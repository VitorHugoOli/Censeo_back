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
    token = Token.objects.get(key=request.auth)
    user = User.objects.get(pk=token.user.pk)
    prof = Professor.objects.get(user=user)
    context: dict = {'categorias': {}}
    try:
        curso = Curso.objects.get(professor_coordenador=prof)
        context['categorias'][curso.codigo] = [
            {'id': curso.id, 'sigla': curso.codigo, 'nome': curso.nome, 'tipo': 'curso'}]
    except ObjectDoesNotExist as ex:
        pass
    prof_turma = ProfessorHasTurma.objects.filter(professor=prof)
    turmas = []
    for i in prof_turma:
        turmas.append(Turma.objects.get(id=i.turma.id))
    for i in turmas:
        disp = Disciplina.objects.get(id=i.disciplina.id)
        if context['categorias'].__contains__(disp.codigo):
            context['categorias'][disp.codigo].append(
                {'id': i.id, 'sigla': disp.sigla, 'nome': disp.nome, 'codigo': i.codigo, 'tipo': 'materia'})
        else:
            context['categorias'][disp.codigo] = [
                {'id': i.id, 'sigla': disp.sigla, 'nome': disp.nome, 'codigo': i.codigo, 'tipo': 'materia'}]
    return Response({'status': True, **context})
