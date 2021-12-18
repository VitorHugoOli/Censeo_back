# Create your views here.
import random
import decimal
from datetime import datetime, timedelta

import dateutil.parser
import pytz
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Avg, Q
from pytz import timezone
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.Enums import tipo_qualificativo, relevancia_points
from Utils.Except import generic_except
from Utils.Parsers import dayToEnum
from Utils.SetInterval import set_interval
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from aula.models import Aula, Teorica
from avaliacao.models import Avaliacao, Caracteristica, Resposta
from avatar.models import AvatarHasAluno, Avatar
from curso.models import Disciplina
from curso.serializers import DisciplinaSerializer
from professor.models import Professor
from turma.models import Turma, DiasFixos, ProfessorHasTurma, AlunoHasTurma, SugestaoTurma, TopicaTurma
from turma.serializers import TurmaSerializer, DiasFixosSerializer, SugestaoTurmaSerializer, TopicaTurmaSerializer
from user.models import User
import statistics


class TurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request: Request, *args, **kwargs):
        token = Token.objects.get(key=request.auth)
        user = User.objects.get(pk=token.user.pk)
        if "Professor" == user.tipo_user:
            prof = Professor.objects.get(user=user)
            prof_turmasList = ProfessorHasTurma.objects.filter(professor=prof)
            context = {"turmas": []}
            for prof_turma in prof_turmasList:
                turma: Turma = Turma.objects.get(id=prof_turma.turma.id)
                jsonTurma = TurmaSerializer(turma).data
                disciplina: Disciplina = Disciplina.objects.get(id=turma.disciplina.id)
                jsonTurma["disciplina"] = DisciplinaSerializer(disciplina, context={'request': request}).data
                try:
                    horarios: DiasFixos = DiasFixos.objects.filter(turma=turma)
                    jsonTurma["horarios"] = DiasFixosSerializer(horarios, many=True).data
                except ObjectDoesNotExist as ex:
                    print(">>> This Class Don't have schedule time yet")
                    pass
                context["turmas"].append(jsonTurma)
            return Response({"status": True, **context})
        else:
            return Response({"status": False, "message": "Hey it's a trap, you're not a professor"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_turma_stats(request: Request, *args, **kwargs):
    tipo_resps = [None or '', 'pessima', 'ruim', 'regular', 'boa', 'perfeita']
    characteristics = Caracteristica.objects.filter()

    user = request.user

    if "Professor" == user.tipo_user:
        context = prof_turmas_stats(characteristics, tipo_resps, user)
    else:
        context = aluno_turmas_stats(characteristics, tipo_resps, user)

    return Response({"status": True, "turmas": context})


def prof_turmas_stats(characteristics, tipo_resps, user):
    turmas_prof = Turma.objects.filter(professorhasturma__professor__user=user)

    context = TurmaSerializer(turmas_prof, many=True).data
    for index, turma in enumerate(turmas_prof):
        disciplina = DisciplinaSerializer(turma.disciplina).data
        del disciplina['id']
        context[index] = {**context[index], **disciplina}
        context[index]['stats'] = {}
        for i in characteristics:
            respostas = Resposta.objects.filter(avaliacao__aula__turma=turma, pergunta__caracteristica=i, tipo_resposta='qualificativa').values_list(
                'resposta_qualificativa', flat=True)
            if len(respostas) > 0:
                context[index]['stats'][i.qualificacao] = statistics.mean([tipo_resps.index(i) for i in respostas])
        context[index]['avals_count'] = Avaliacao.objects.filter(aula__turma=turma).count()
    return context


def aluno_turmas_stats(characteristics, tipo_resps, user):
    turmas_aluno = Turma.objects.filter(alunohasturma__aluno__user=user)

    context = TurmaSerializer(turmas_aluno, many=True).data

    for index, turma in enumerate(turmas_aluno):

        disciplina = DisciplinaSerializer(turma.disciplina).data

        del disciplina['id']

        context[index] = {**context[index], **disciplina}
        context[index]['stats'] = {}

        for i in characteristics:
            respostas = Resposta.objects.filter(avaliacao__aula__turma=turma, pergunta__caracteristica=i, tipo_resposta='qualificativa', avaliacao_aluno__user=user).values_list(
                'resposta_qualificativa', flat=True)
            if len(respostas) > 0:
                context[index]['stats'][i.qualificacao] = sum([tipo_resps.index(i) for i in respostas]) / len(respostas)
        context[index]['avals_count'] = Avaliacao.objects.filter(aula__turma=turma).count()

    return context


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def turma_stats(request: Request, *args, **kwargs):
    user = request.user
    id = kwargs['id']
    context = {'aulas': {}}

    if "Professor" == user.tipo_user:
        _turma_stats(context, id, None)
    else:
        _turma_stats(context, id, user.id)

    return Response(context, status=200)


def _turma_stats(context, id, aluno_id):
    aulas: QuerySet[Aula] = Aula.objects.filter(turma_id=id).order_by('-end_time')
    aula_context = context['aulas']
    aula_context['total'] = len(aulas)
    aula_context['done'] = len(aulas.filter(end_time__isnull=False))
    aula_context['teorica'] = len(aulas.filter(tipo_aula='teorica'))
    aula_context['prova'] = len(aulas.filter(tipo_aula='prova'))
    aula_context['trabalho'] = len(aulas.filter(tipo_aula='trabalho'))
    aula_context['excursao'] = len(aulas.filter(tipo_aula='excursao'))
    tipo_resps = [None or '', 'pessima', 'ruim', 'regular', 'boa', 'perfeita']

    alunos = AlunoHasTurma.objects.filter(turma_id=id).order_by('-xp')
    context['rank'] = []
    for i in alunos:
        aluno_serialize = AlunoSerializer(i.aluno).data
        aluno_serialize['turma_xp'] = i.xp
        context['rank'].append(aluno_serialize)

    characteristics = Caracteristica.objects.filter()

    for j in characteristics:
        label = j.qualificacao.split(' ')[0].split('/')[0]
        context[label] = {}

        if aluno_id is not None:
            print("Bingo")
            respostas = Resposta.objects.filter(avaliacao__aula__turma__id=id, pergunta__caracteristica=j, tipo_resposta='qualificativa', avaliacao__aluno__id=aluno_id)
        else:
            respostas = Resposta.objects.filter(avaliacao__aula__turma__id=id, pergunta__caracteristica=j, tipo_resposta='qualificativa')

        respostas = respostas.values_list('resposta_qualificativa', flat=True)
        respostas = [tipo_resps.index(i) for i in respostas]
        context[label]['len'] = len(respostas)

        if len(respostas) > 0:
            context[label]['media'] = statistics.mean(respostas)
            context[label]['desvio'] = statistics.pstdev(respostas)
            context[label]['variancia'] = statistics.pvariance(respostas)
        else:
            context[label]['media'] = 0
            context[label]['desvio'] = 0
            context[label]['variancia'] = 0

        context[label]['ultimas_dez_medias'] = {}

    for i in aulas.filter(end_time__isnull=False)[0:10]:
        respostas = Resposta.objects.filter(avaliacao__aula__turma__id=id, tipo_resposta='qualificativa', avaliacao_aula=i)
        if len(respostas) > 0:
            for j in characteristics:
                label = j.qualificacao.split(' ')[0].split('/')[0]
                respostas_charact = respostas.filter(pergunta__caracteristica=j).values_list('resposta_qualificativa', flat=True)
                context[label]['ultimas_dez_medias'][i.end_time.strftime("%d/%m")] = statistics.mean([tipo_resps.index(i) for i in respostas_charact])


class DiasFixosViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DiasFixos.objects.all()
    serializer_class = DiasFixosSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:
            if "idTurma" in data and "schedules" in data:
                turma = Turma.objects.get(id=data["idTurma"])
                fixed_days = DiasFixos.objects.filter(turma=turma).values_list('id', flat=True)
                schedule_received: list = data['schedules']

                for i in fixed_days:
                    is_active = False
                    for j in schedule_received:
                        if i == j['id']:
                            is_active = True
                    if not is_active:
                        DiasFixos.objects.get(id=i).delete()

                for i in schedule_received:
                    id = i['id']
                    if id is None:
                        dia = DiasFixos(
                            turma=turma,
                            dia=DiasFixos.NormalDayToTipoDia(i['dia']),
                            horario=dateutil.parser.parse(i['horario']),
                            sala=i['sala'],
                            is_assincrona=i['is_assincrona'],
                        )
                        if dia.is_assincrona:
                            dia.days_to_end = i['days_to_end']
                        dia.save()
                    elif id in fixed_days:
                        dia: DiasFixos = DiasFixos.objects.get(id=id)
                        aulas: QuerySet[Aula] = Aula.objects.filter(turma=turma,
                                                                    sala=dia.sala,
                                                                    dia_horario__hour=dia.horario.hour,
                                                                    dia_horario__minute=dia.horario.minute)
                        novo_horario = dateutil.parser.parse(i['horario'])

                        if dia.horario != novo_horario:

                            for j in aulas:
                                replace_date = datetime(year=j.dia_horario.year, month=j.dia_horario.month,
                                                        day=j.dia_horario.day, hour=novo_horario.hour,
                                                        minute=novo_horario.minute)
                                j.dia_horario = replace_date
                                j.save()

                            dia.horario = novo_horario

                        if dia.is_assincrona != i['is_assincrona']:
                            dia.is_assincrona = i['is_assincrona']
                            aulas.update(
                                is_assincrona=i['is_assincrona']
                            )
                            if i['is_assincrona'] and dia.days_to_end != i['days_to_end']:
                                dia.days_to_end = i['days_to_end']
                                for j in aulas:
                                    j.end_time = j.dia_horario + timedelta(days=int(i['days_to_end']))

                        if dia.sala != i['sala']:
                            dia.sala = i['sala']
                            aulas.update(
                                sala=i['sala']
                            )
                        dia.save(edit=True)

                return Response({"status": True})
            else:
                return Response({"status": False, "error": "Algo está faltando"})
        except Exception as ex:
            return generic_except(ex)


# if i.__contains__('id'):
#     if i['id']:
#         if i['id'] > 0:
#             # Editando
#             dia = DiasFixos.objects.get(id=i['id'], turma_id=turma.id)
#             if i['horario'] is not None:
#                 newTime = dateutil.parser.parse(i['horario'])
#                 date1 = datetime(dia.horario.year, dia.horario.month, dia.horario.day,
#                                  dia.horario.hour,
#                                  dia.horario.minute)
#                 date2 = datetime(newTime.year, newTime.month, newTime.day, newTime.hour,
#                                  newTime.minute)
#                 if date1 != date2 or dia.sala != i['sala']:
#                     aulas = Aula.objects.filter(turma=turma,
#                                                 sala=dia.sala,
#                                                 dia_horario__hour=dia.horario.hour,
#                                                 dia_horario__minute=dia.horario.minute)
#                     dia.horario = newTime
#                     dia.sala = i['sala']
#
#                     for aula in aulas:
#                         aula.dia_horario = datetime(aula.dia_horario.year, aula.dia_horario.month,
#                                                     aula.dia_horario.day, newTime.hour,
#                                                     newTime.minute)
#                         aula.sala = dia.sala
#                         aula.save()
#
#                     dia.save(edit=True)
#             else:
#                 # Deletando
#                 dia.delete()
#         elif i['id'] < 0:
#             # Lixo de memoria
#             # Esse Dia provavelmente já foi salvo no BD e está vindo alguma requisição que não foi atualizada no front
#             pass
#     else:
#         # Criando
#         dia = DiasFixos(
#             turma=turma,
#             dia=dayToEnum(i['dia'][0:3]),
#             horario=dateutil.parser.parse(i['horario']),
#             sala=i['sala']
#         )
#         dia.save()
# else:
#     Response({"status": False, "error": "Algo está faltando"})


class TopicaTurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = TopicaTurma.objects.all()
    serializer_class = TopicaTurmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request: Request, *args, **kwargs):
        try:
            id = kwargs['pk']
            topicos = TopicaTurma.objects.filter(turma_id=id)
            return Response({"status": True, 'topicos': self.serializer_class(topicos, many=True).data})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            data = request.data
            turma = Turma.objects.get(id=id)
            for i in data:
                if int(i['id']) >= 0:
                    topico = TopicaTurma.objects.get(id=i['id'])
                    if not topico.topico == i['topico']:
                        topico.topico = i['topico']
                        topico.save()
                else:
                    TopicaTurma(
                        topico=i['topico'],
                        turma=turma
                    ).save()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)

    def destroy(self, request, *args, **kwargs):
        try:
            TopicaTurma.objects.get(id=kwargs['pk']).delete()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)


class SugestaoTurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SugestaoTurma.objects.all()
    serializer_class = SugestaoTurmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:

            if 'sugestao' in data and 'titulo' in data:
                aluno = Aluno.objects.get(user=request.user)
                topico: TopicaTurma = TopicaTurma.objects.get(id=data['topico'])
                SugestaoTurma(
                    sugestao=data['sugestao'],
                    titulo=data['titulo'],
                    data=datetime.today(),
                    topico=topico,
                    turma=topico.turma,
                    aluno=aluno
                ).save()
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)

    def retrieve(self, request, *args, **kwargs):
        try:
            if request.user.tipo_user == 'Professor':
                sug = SugestaoTurma.objects.filter(turma=kwargs['pk'])
            else:
                aluno = Aluno.objects.get(user=request.user)
                sug = SugestaoTurma.objects.filter(turma=kwargs['pk'], aluno=aluno)
            sug = sug.order_by('relevancia', 'data')

            return Response({"status": True,
                             'suguestoes': self.serializer_class(sug, many=True).data})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id = kwargs['pk']
            relevance = request.data['relevance']
            sug = SugestaoTurma.objects.get(id=id)
            aluno = AlunoHasTurma.objects.get(aluno=sug.aluno, turma_id=sug.turma)
            if sug.relevancia is not None:
                aluno.xp -= decimal.Decimal(relevancia_points[sug.relevancia])
            sug.relevancia = relevance
            sug.save()
            aluno.xp += decimal.Decimal(relevancia_points[relevance])
            aluno.save()
            return Response({"status": True})
        except Exception as ex:
            return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pupils_list(request: Request, id: int):
    try:
        try:
            alunos_turma: QuerySet[AlunoHasTurma] = AlunoHasTurma.objects.filter(turma_id=id)
            alunos = []
            # Todo: Criar query para melhor velocidade
            for i in alunos_turma:
                aluno = Aluno.objects.get(id=i.aluno_id)
                data = AlunoSerializer(aluno).data
                data['xp'] = i.xp
                avatar_aluno: AvatarHasAluno = AvatarHasAluno.objects.filter(aluno=aluno, is_active=True).first()
                if avatar_aluno:
                    data['perfilPhoto'] = avatar_aluno.avatar.url
                alunos.append(data)
            print(alunos)
            return Response({"status": True, "alunos": alunos})
        except ObjectDoesNotExist as ex:
            print(">>> Wasn't Possible find the Turma")
            return Response({"status": False, "message": "Não foi possivel achar a turma"})


    except Exception as ex:
        return generic_except(ex)


def check_time_for_open_class():
    diferenca = timezone('America/Sao_Paulo')
    print("---> Checking class " + datetime.now().astimezone(diferenca).ctime())
    try:
        query = Aula.objects.all()
        today = datetime.now().astimezone(diferenca)
        aulas: QuerySet[Aula] = query.filter(dia_horario__year=today.year, dia_horario__month=today.month,
                                             dia_horario__day=today.day,
                                             dia_horario__hour=today.hour, dia_horario__minute=today.minute)

        # Check the sync class that need to be open for the professor
        aulas.filter(is_assincrona=False).update(is_aberta_class=True)

        # Check async class that need to be open to avaliation
        async_class = aulas.filter(is_assincrona=True)
        check_tema_tipo(async_class, today, sync=False)
        async_class.update(is_aberta_avaliacao=True, is_aberta_class=False)

        # Check sync class that need to be open to avaliation
        will_open_aval: QuerySet[Aula] = query.filter(is_aberta_class=True, is_assincrona=False, dia_horario__year=today.year, dia_horario__month=today.month,
                                                      dia_horario__day=today.day,
                                                      dia_horario__hour=(today - timedelta(hours=2)).hour, dia_horario__minute=today.minute)

        check_tema_tipo(will_open_aval, today, sync=True)

        will_open_aval.update(is_aberta_avaliacao=True, is_aberta_class=False, end_time=datetime.now().astimezone(diferenca))

        # Check sync and async class that need to be end
        # Closes any classes in 7 days
        will_end_class: QuerySet[Aula] = query.filter(Q(dia_horario__year=today.year, dia_horario__month=today.month, dia_horario__day=(today - timedelta(days=7)).day,
                                                        dia_horario__hour=today.hour, dia_horario__minute=today.minute) |
                                                      Q(end_time__year=today.year, end_time__month=today.month, end_time__day=today.day,
                                                        end_time__hour=today.hour, end_time__minute=today.minute),
                                                      is_aberta_avaliacao=True)

        will_end_class.filter(is_assincrona=True, end_time__isnull=True).update(end_time=today)
        will_end_class.update(is_aberta_avaliacao=False, is_aberta_class=False)

        print("---> Verification successful")
    except Exception as ex:
        print("---x Não foi possivel checar todas as aulas")
        print(ex)


def check_tema_tipo(classes, today, sync=True):
    # Check if the class that will be open to evaluation have a tema and tipo, in toher way, it's create a tema and tipo for the class
    classes.filter(Q(tema__isnull=True) | Q(tema='')).update(tema=f'Aula {"Sincrona" if sync else "Assincrona"} - {str(today.day)}/{str(today.month)}')
    classes_teo = classes.filter(Q(tipo_aula__isnull=True) | Q(tipo_aula=''))
    teo_list_create = [Teorica(aula=i) for i in classes_teo]
    teo = Teorica.objects.bulk_create(teo_list_create)
    classes_teo.update(tipo_aula='teorica')
