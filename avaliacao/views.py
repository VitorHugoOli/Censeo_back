# Create your views here.
import decimal
import math
from datetime import datetime, timedelta
from decimal import Decimal

from django.db.models import QuerySet, Sum, Avg, Count, F
from django.utils import timezone
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from Utils.Except import generic_except
from Utils.Pontos import PONTOS_AULA
from aluno.models import Aluno
from aula.models import Aula
from avaliacao.models import Avaliacao, Pergunta, Resposta
from avaliacao.serializers import AvaliacaoSerializer, PerguntaSerializer, RespostaSerializer
from turma.models import AlunoHasTurma, Turma
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

                # Caso seja a ultima resposta de uma avaliação
                if data.__contains__('end'):
                    aval.end_time = timezone.now()
                    aval.completa = True

                    aluno_turma = AlunoHasTurma.objects.get(aluno=aval.aluno, turma=aval.aula.turma)
                    aluno_turma.xp += decimal.Decimal(CalcAvalPontuacao(aval.aula.end_time, aval.end_time))

                    aluno = Aluno.objects.get(id=aval.aluno.id)
                    aluno.xp += aluno_turma.xp

                    aluno.save()
                    aluno_turma.save()
                    aval.save()

                return Response({'status': True})
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
        except Exception as ex:
            return generic_except(ex)


def CalcAvalPontuacao(end_aula: datetime, end_aval: datetime):
    difference = end_aval - end_aula
    minutes = difference.total_seconds() / 60
    if minutes < 20:
        return PONTOS_AULA
    elif minutes < 60:
        return PONTOS_AULA * 0.60
    else:
        hours = math.floor(minutes / 60)
        return (PONTOS_AULA * 0.60) * pow(0.90, hours)


def CalcPontuacaoDia(aluno):
    today = datetime.today() - timedelta(2)
    avals: QuerySet[Avaliacao] = Avaliacao.objects.filter(end_time__date=today,
                                                          aluno=aluno,
                                                          completa=True)
    print(avals)
    avg: decimal.Decimal = avals.aggregate(Avg("pontos"))['pontos__avg']

    # if avg > 20:
    #     print("Fogo")
    # elif avg > 10:
    #     print("medio")
    # else:
    #     print("Snow")

    return avg


def CalcWonWeekRewards(aluno):
    today = datetime.today()
    startWeek = today - timedelta(7)

    avals = Avaliacao.objects.filter(end_time__gte=startWeek,
                                     aluno=aluno)

    avg: decimal.Decimal = avals.aggregate(Avg("pontos"))['pontos__avg']

    # if avg == 25:
    #     print('shine')
    # elif avg>20:
    #     print('normal')
    # else
    #     print('nothing')

    return avg


def CalcGeneralRank():
    alunos = AlunoHasTurma.objects.values_list("aluno", flat=True).annotate(num_turmas=Count("id"))
    rank = Aluno.objects.filter(id__in=list(alunos)).annotate(nome=F('user__nome')).values('id', 'nome', 'xp')
    return rank


def CalcGeneralRankByQuantSubj(aluno):
    countTurmas: QuerySet = AlunoHasTurma.objects.filter(aluno=aluno).count()
    alunos = AlunoHasTurma.objects.values_list("aluno", flat=True).annotate(num_turmas=Count("id")).filter(
        num_turmas=countTurmas)
    rank = Aluno.objects.filter(id__in=list(alunos)).annotate(nome=F('user__nome')).values('id', 'nome', 'xp')
    print(rank)
    return rank


def CalcRankTurma(turma: Turma):
    rank = AlunoHasTurma.objects.filter(turma=turma).annotate(nome=F('aluno__user__nome')).values('aluno_id',
                                                                                                  'nome',
                                                                                                  'xp')
    return rank


def weekRoutine():
    alunos = Aluno.objects.all()
    for i in alunos:
        CalcPontuacaoDia(i)


def rewardsRoutine():
    today = datetime.now()
    # avatar_shiny = Avatar.object.get(date__date=today, isShiny=True)
    # avatar = Avatar.object.get(date__date=today, isShiny=False)
    # if len(avatares) > 0:
    #     alunos = Aluno.objects.all()
    #     for i in alunos:
    #         pontos = CalcWonWeekRewards(i)
    #         if pontos == 25:
    #             AvatarHasAluno(
    #                 avatar=avatar_shiny,
    #                 aluno=i
    #             ).save()
    #
    #         if 20 <= pontos < 25:
    #             AvatarHasAluno(
    #                 avatar=avatar,
    #                 aluno=i
    #             ).save()
