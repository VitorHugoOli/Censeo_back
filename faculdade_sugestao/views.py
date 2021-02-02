# Create your views here.
from datetime import datetime

from rest_framework import viewsets, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.Except import generic_except
from aluno.models import Aluno
from faculdade.models import Faculdade
from faculdade_sugestao.models import TopicoFaculdade, SugestaoFaculdade
from faculdade_sugestao.serializers import TopicoFaculdadeSerializer, SugestaoFaculdadeSerializer


class TopicoFaculdadeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TopicoFaculdade.objects.all()
    serializer_class = TopicoFaculdadeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request: Request, *args, **kwargs):
        try:
            id = kwargs['pk']
            topicos = TopicoFaculdade.objects.filter(faculdade_id=id)
            return Response({"status": True, 'topicos': self.serializer_class(topicos, many=True).data})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            data = request.data
            turma = Faculdade.objects.get(id=id)
            for i in data:
                if int(i['id']) >= 0:
                    topico = TopicoFaculdade.objects.get(id=i['id'])
                    if not topico.topico == i['topico']:
                        topico.topico = i['topico']
                        topico.save()
                else:
                    TopicoFaculdade(
                        topico=i['topico'],
                        turma=turma
                    ).save()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)

    def destroy(self, request, *args, **kwargs):
        try:
            TopicoFaculdade.objects.get(id=kwargs['pk']).delete()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)


class SugestaoFaculdadeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SugestaoFaculdade.objects.all()
    serializer_class = SugestaoFaculdadeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:

            if 'sugestao' in data and 'titulo' in data:
                aluno = Aluno.objects.get(user=request.user)
                topico: TopicoFaculdade = TopicoFaculdade.objects.get(id=data['topico'])
                SugestaoFaculdade(
                    sugestao=data['sugestao'],
                    titulo=data['titulo'],
                    data=datetime.today(),
                    topico=topico,
                    faculdade=topico.faculdade,
                    aluno=aluno,
                    user=aluno.user
                ).save()
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)

    def retrieve(self, request, *args, **kwargs):
        try:
            if request.user.tipo_user == 'Professor':
                sug = SugestaoFaculdade.objects.filter(faculdade_id=kwargs['pk'])
            else:
                aluno = Aluno.objects.get(user=request.user)
                sug = SugestaoFaculdade.objects.filter(faculdade_id=kwargs['pk'], aluno=aluno)
            sug = sug.order_by('-data')

            return Response({"status": True, 'suguestoes': self.serializer_class(sug, many=True).data})
        except Exception as ex:
            return generic_except(ex)
