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
from aluno.models import Aluno, StrikeDia
from aula.models import Aula
from avaliacao.models import Avaliacao, Pergunta, Resposta, Caracteristica
from avaliacao.serializers import AvaliacaoSerializer, PerguntaSerializer, RespostaSerializer
from avatar.models import AvatarHasAluno, Avatar
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
                except Exception as ex:
                    aval = Avaliacao(
                        aula=aula,
                        aluno=aluno,
                        completa=False,
                    )
                    aval.save()

                context = {'avaliacao': self.serializer_class(aval).data}
                context['avaliacao']['tipo_aula'] = aula.tipo_aula

                perguntas = []
                caracteristicas: QuerySet


                if aula.tipo_aula == 'trabalho' or aula.tipo_aula == 'prova':
                    caracteristicas = Caracteristica.objects.filter(id__in=[1, 5, 6, 9, 10])
                else:
                    caracteristicas = Caracteristica.objects.all()

                if resp is not None:
                    caracteristicas = caracteristicas.exclude(id__in=resp.values_list("pergunta__caracteristica", flat=True))

                for i in caracteristicas:
                    if (aula.tipo_aula == 'trabalho' or aula.tipo_aula == 'prova') and i.id == 10:
                        perguntas = perguntas + list(Pergunta.objects.filter(caracteristica=i).order_by("?"))[0:3]
                    else:
                        perguntas.append(Pergunta.objects.filter(caracteristica=i).order_by("?").first())

                context['avaliacao']['perguntas'] = PerguntaSerializer(perguntas, many=True).data

                for i in context['avaliacao']['perguntas']:
                    i['caracteristica'] = i['caracteristica']['qualificacao']

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

                    if aval.aula.is_assincrona is False:
                        aval.pontos = decimal.Decimal(CalcAvalPontuacao(aval.aula.end_time, aval.end_time))
                    else:
                        aval.pontos = 25
                    aval.save()

                    aluno_turma = AlunoHasTurma.objects.get(aluno=aval.aluno, turma=aval.aula.turma)
                    aluno_turma.xp += aval.pontos
                    aluno_turma.save()

                    if aval.aula.is_assincrona is False:
                        aluno = Aluno.objects.get(id=aval.aluno.id)
                        aluno.xp += aluno_turma.xp
                        aluno.save()

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
    today = datetime.today()
    turmas = AlunoHasTurma.objects.filter(aluno=aluno).values('turma')
    aulas = Aula.objects.filter(end_time__date=today, turma__in=turmas, is_assincrona=False, is_aberta_avaliacao=True)
    avals: QuerySet[Avaliacao] = Avaliacao.objects.filter(aluno=aluno,
                                                          aula__in=aulas,
                                                          completa=True)
    if len(aulas) != 0:
        avg: decimal.Decimal = avals.aggregate(Sum("pontos"))['pontos__sum'] / len(aulas)
    else:
        return -1  # Não houve aulas

    return avg


def CalcWonWeekRewards(aluno):
    today = datetime.today()
    startWeek = today - timedelta(7)

    turmas = AlunoHasTurma.objects.filter(aluno=aluno).values('turma')
    aulas = Aula.objects.filter(end_time__gte=startWeek, turma__in=turmas, is_aberta_avaliacao=True)
    avals = Avaliacao.objects.filter(aula__in=aulas, completa=True, aluno=aluno)

    avg = avals.aggregate(Sum("pontos"))['pontos__sum'] / len(aulas)
    if avg is None:
        return 0
    else:
        return float(avg)

    # if avg == 25:
    #     print('shine')
    # elif avg>20:
    #     print('normal')
    # else
    #     print('nothing')


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
        pontos = CalcPontuacaoDia(i)
        if pontos == -1:
            StrikeDia(
                date=datetime.today(),
                aluno=i
            ).save()
            return
        strike = ''
        if pontos > 20:
            strike = 'fire'
        elif pontos > 10:
            strike = 'cold_fire'
        else:
            strike = 'snow'
        StrikeDia.objects.create(
            strike=strike,
            date=datetime.today(),
            aluno=i
        )


def rewardsRoutine():
    print("--> Start Week Rewards")
    today = datetime.now()
    avatar_shiny = None
    avatar = None
    try:
        avatar = Avatar.objects.get(date=today, is_shiny=False)
    except Avatar.DoesNotExist as ex:
        print(ex)
    try:
        avatar_shiny = Avatar.objects.get(date=today, is_shiny=True)
    except Avatar.DoesNotExist as ex:
        print(ex)

    if avatar is not None or avatar_shiny is not None:
        alunos = Aluno.objects.all()
        for i in alunos:
            pontos = CalcWonWeekRewards(i)
            print(f"pontos-> {pontos}")
            if pontos == 25.0 and avatar_shiny is not None:
                AvatarHasAluno(
                    avatar=avatar_shiny,
                    aluno=i
                ).save()

            if 20.0 >= pontos and avatar is not None:
                AvatarHasAluno(
                    avatar=avatar,
                    aluno=i
                ).save()
    print("--> Week Rewards successful")
