# Create your views here.
from datetime import datetime

import dateutil.parser
from django.core.exceptions import ObjectDoesNotExist
from pytz import timezone
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.Except import generic_except
from Utils.Parsers import dayToEnum
from Utils.SetInterval import set_interval
from aluno.serializers import AlunoSerializer
from aula.models import Aula
from curso.models import Disciplina
from curso.serializers import DisciplinaSerializer
from professor.models import Professor
from turma.models import Turma, DiasFixos, ProfessorHasTurma, AlunoHasTurma, SugestaoTurma, TopicaTurma
from turma.serializers import TurmaSerializer, DiasFixosSerializer, SugestaoTurmaSerializer, TopicaTurmaSerializer
from user.models import User


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
            if data.__contains__("idTurma") and data.__contains__("schedules"):
                turma = Turma.objects.get(id=data["idTurma"])
                scheduleReceived: list = data['schedules']
                for i in scheduleReceived:
                    if i.__contains__('id'):
                        if i['id']:
                            if i['id'] > 0:
                                # Editando
                                dia = DiasFixos.objects.get(id=i['id'], turma_id=turma.id)
                                if i['horario'] is not None:
                                    newTime = dateutil.parser.parse(i['horario'])
                                    date1 = datetime(dia.horario.year, dia.horario.month, dia.horario.day,
                                                     dia.horario.hour,
                                                     dia.horario.minute)
                                    date2 = datetime(newTime.year, newTime.month, newTime.day, newTime.hour,
                                                     newTime.minute)
                                    if date1 != date2 or dia.sala != i['sala']:
                                        aulas = Aula.objects.filter(turma=turma,
                                                                    sala=dia.sala,
                                                                    dia_horario__hour=dia.horario.hour,
                                                                    dia_horario__minute=dia.horario.minute)
                                        dia.horario = newTime
                                        dia.sala = i['sala']

                                        for aula in aulas:
                                            aula.dia_horario = datetime(aula.dia_horario.year, aula.dia_horario.month,
                                                                        aula.dia_horario.day, newTime.hour,
                                                                        newTime.minute)
                                            aula.sala = dia.sala
                                            aula.save()

                                        dia.save(edit=True)
                                else:
                                    # Deletando
                                    dia.delete()
                            elif i['id'] < 0:
                                # Lixo de memoria
                                # Esse Dia provavelmente já foi salvo no BD e está vindo alguma requisição que não foi atualizada no front
                                pass
                        else:
                            # Criando
                            dia = DiasFixos(
                                turma=turma,
                                dia=dayToEnum(i['dia'][0:3]),
                                horario=dateutil.parser.parse(i['horario']),
                                sala=i['sala']
                            )
                            dia.save()
                    else:
                        Response({"status": False, "error": "Algo está faltando"})
                return Response({"status": True})
            else:
                return Response({"status": False, "error": "Algo está faltando"})
        except Exception as ex:
            return generic_except(ex)


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

    def retrieve(self, request, *args, **kwargs):
        try:
            sug = SugestaoTurma.objects.filter(topica_turma_turma_id=kwargs['pk'])
            return Response({"status": True, 'suguestoes': self.serializer_class(sug, many=True).data})
        except Exception as ex:
            return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pupils_list(request: Request, id: int):
    try:
        alunos = []

        try:
            alunos_turma = AlunoHasTurma.objects.filter(turma_id=id)
        except ObjectDoesNotExist as ex:
            print(">>> Wasn't Possible find the Turma")
            return Response({"status": False, "message": "Não foi possivel achar a turma"})

        for i in alunos_turma:
            alunos.append(i.aluno)
        return Response({"status": True, "alunos": AlunoSerializer(alunos, many=True).data})
    except Exception as ex:
        return generic_except(ex)


def checkTimeForOpenClass():
    diferenca = timezone('America/Sao_Paulo')
    querry = Aula.objects.all()
    today = datetime.now().astimezone(diferenca)
    print(today.strftime("%Y:%m:%d"))
    print(today.strftime("%H:%M:%S"))
    aulas = querry.filter(dia_horario__year=today.year, dia_horario__month=today.month, dia_horario__day=today.day,
                          dia_horario__hour=today.hour, dia_horario__minute=today.minute)
    print(aulas)
    for i in aulas:
        i.is_aberta_class = True
        i.save()
    print("--- checked Class Open")


set_interval(checkTimeForOpenClass, 60)
