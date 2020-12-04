# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.Except import generic_except
from aluno.models import Aluno, TopicoSugestaoCurso, SugestaoCurso
from aluno.serializers import AlunoSerializer, TopicoSugestaoCursoSerializer, SugestaoCursoSerializer
from curso.models import Curso


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
            turma = Curso.objects.get(id=id)
            for i in data:
                if int(i['id']) >= 0:
                    topico = TopicoSugestaoCurso.objects.get(id=i['id'])
                    if not topico.topico == i['topico']:
                        topico.topico = i['topico']
                        topico.save()
                else:
                    TopicoSugestaoCurso(
                        topico=i['topico'],
                        turma=turma
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

    def retrieve(self, request, *args, **kwargs):
        try:
            sug = SugestaoCurso.objects.filter(topico_sugestao_curso_id=kwargs['pk'])
            print(sug)
            return Response({"status": True, 'suguestoes': self.serializer_class(sug, many=True).data})
        except Exception as ex:
            return generic_except(ex)
