# Create your views here.
from datetime import datetime, timedelta

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.Except import generic_except
from aluno.models import Aluno, TopicoSugestaoCurso, SugestaoCurso, StrikeDia
from aluno.serializers import AlunoSerializer, TopicoSugestaoCursoSerializer, SugestaoCursoSerializer
from curso.models import Curso, Disciplina
from turma.models import AlunoHasTurma


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicoSugestaoCursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TopicoSugestaoCurso.objects.all()
    serializer_class = TopicoSugestaoCursoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request: Request, *args, **kwargs):
        try:
            id = kwargs['pk']
            topicos = TopicoSugestaoCurso.objects.filter(curso_id=id)
            return Response({"status": True, 'topicos': self.serializer_class(topicos, many=True).data})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            data = request.data
            curso = Curso.objects.get(id=id)
            for i in data:
                if int(i['id']) >= 0:
                    topico = TopicoSugestaoCurso.objects.get(id=i['id'])
                    if not topico.topico == i['topico']:
                        topico.topico = i['topico']
                        topico.save()
                else:
                    TopicoSugestaoCurso(
                        topico=i['topico'],
                        curso=curso
                    ).save()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)

    def destroy(self, request, *args, **kwargs):
        try:
            TopicoSugestaoCurso.objects.get(id=kwargs['pk']).delete()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)


class SugestaoCursoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SugestaoCurso.objects.all()
    serializer_class = SugestaoCursoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:

            if 'sugestao' in data and 'titulo' in data:
                aluno = Aluno.objects.get(user=request.user)
                topico: TopicoSugestaoCurso = TopicoSugestaoCurso.objects.get(id=data['topico'])
                SugestaoCurso(
                    sugestao=data['sugestao'],
                    titulo=data['titulo'],
                    data=datetime.today(),
                    topico=topico,
                    curso=topico.curso,
                    aluno=aluno
                ).save()
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)

    def retrieve(self, request, *args, **kwargs):
        try:
            sug: QuerySet
            if request.user.tipo_user == 'Professor':
                sug = SugestaoCurso.objects.filter(curso_id=kwargs['pk'])
            else:
                aluno = Aluno.objects.get(user=request.user)
                sug = SugestaoCurso.objects.filter(curso_id=kwargs['pk'], aluno=aluno)
            sug = sug.order_by('-data')
            return Response({"status": True, 'suguestoes': self.serializer_class(sug, many=True).data})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            relevance = request.data['relevance']
            sug = SugestaoCurso.objects.get(id=id)
            sug.relevancia = relevance
            sug.save()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_suggestions_categories(request):
    aluno = Aluno.objects.get(user=request.user)
    context: dict = {'categorias': {}}

    try:
        curso = Curso.objects.get(id=aluno.curso_idcurso.id)
        context['categorias']['Faculdade'] = [
            {'id': curso.id, 'sigla': curso.faculdade.sigla, 'nome': curso.faculdade.nome, 'tipo': 'facu'}]
        context['categorias']['Curso'] = [
            {'id': curso.id, 'sigla': curso.codigo, 'nome': curso.nome, 'tipo': 'curso'}]
    except ObjectDoesNotExist as ex:
        pass

    context['categorias']['Disciplinas'] = []
    aluno_turma = AlunoHasTurma.objects.filter(aluno=aluno)
    for i in aluno_turma:
        turma = i.turma
        disp = Disciplina.objects.get(id=turma.disciplina.id)
        context['categorias']['Disciplinas'].append(
            {'id': turma.id, 'sigla': disp.sigla, 'nome': disp.nome, 'codigo': turma.codigo, 'tipo': 'materia'})

    return Response({'status': True, **context})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_strikes(request):
    context: dict = {"strikes": []}
    today = datetime.today()
    date = today - timedelta(days=today.weekday())
    for i in range(7):
        try:
            strike = StrikeDia.objects.get(aluno__user=request.user, date=date)
            context['strikes'].append(strike.strike)
        except ObjectDoesNotExist as ex:
            context['strikes'].append('')
        date += timedelta(days=1)

    return Response({'status': True, **context})
