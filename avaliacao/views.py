# Create your views here.
from django.db.models import QuerySet
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from Utils.Except import generic_except
from aluno.models import Aluno
from aula.models import Aula
from avaliacao.models import Avaliacao, Pergunta, Resposta
from avaliacao.serializers import AvaliacaoSerializer, PerguntaSerializer, RespostaSerializer
from user.models import User


class AvaliacaoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:
            if data.__contains__('aulaId'):

                aula = Aula.objects.get(id=data['aulaId'])
                token = Token.objects.get(key=request.auth)
                user = User.objects.get(pk=token.user.pk)
                aluno = Aluno.objects.get(user=user)
                resp = None
                try:
                    aval = Avaliacao.objects.get(aula=aula, aluno=aluno)
                    resp = Resposta.objects.filter(avaliacao=aval)
                    print(resp)
                except Exception as ex:
                    aval = Avaliacao(
                        aula=aula,
                        aluno=aluno,
                        completa=False,
                    )
                    aval.save()

                context = {'avaliacao': self.serializer_class(aval).data}
                context['avaliacao']['tipo_aula'] = aula.tipo_aula
                perguntas: QuerySet = Pergunta.objects.filter(tipo_aula=aula.tipo_aula)
                if resp is not None:
                    for i in resp:
                        perguntas = perguntas.exclude(id=i.pergunta.id)

                context['avaliacao']['perguntas'] = PerguntaSerializer(perguntas, many=True).data

                for i in context['avaliacao']['perguntas']:
                    i['caracteristica'] = i['caracteristica']['qualificacao']

                print(context)

                return Response({'status': True, **context})
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        print(request.data)
        return Response({'status': True})


class RespostaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Resposta.objects.all()
    serializer_class = RespostaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        print(data)

        try:
            if data.__contains__('avaliacaoId') and data.__contains__('perguntaId'):
                tipo = data['tipo_resposta']
                resp = data['resposta']
                aval = Avaliacao.objects.get(id=data['avaliacaoId'])
                pergunta = Pergunta.objects.get(id=data['perguntaId'])

                resp_obj = Resposta(
                    tipo_resposta=tipo,
                    avaliacao=aval,
                    avaliacao_aula=aval.aula,
                    avaliacao_aluno=aval.aluno,
                    pergunta=pergunta,
                )

                if tipo == 'binario':
                    resp_obj.resposta_binario = resp
                elif tipo == 'qualificativa':
                    resp_obj.resposta_qualificativa = resp
                elif tipo == 'aberta':
                    resp_obj.resposta_aberta = resp

                resp_obj.save()

                if data.__contains__('end'):
                    aval.completa = True
                    aval.save()

                return Response({'status': True})
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
        except Exception as ex:
            return generic_except(ex)
