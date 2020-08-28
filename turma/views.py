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
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from aula.models import Aula
from curso.models import Disciplina
from curso.serializers import DisciplinaSerializer
from professor.models import Professor
from turma.models import Turma, DiasFixos, ProfessorHasTurma, AlunoHasTurma, SugestaoTurma
from turma.serializers import TurmaSerializer, DiasFixosSerializer, SugestaoTurmaSerializer
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
            prof = Professor.objects.get(user_iduser=user)
            prof_turmasList = ProfessorHasTurma.objects.filter(professor_idprofessor=prof)
            context = {"turmas": []}
            for prof_turma in prof_turmasList:
                turma: Turma = Turma.objects.get(idturma=prof_turma.turma_idturma.idturma)
                jsonTurma = TurmaSerializer(turma).data
                disciplina: Disciplina = Disciplina.objects.get(iddisciplina=turma.disciplina_iddisciplina.iddisciplina)
                jsonTurma["disciplina"] = DisciplinaSerializer(disciplina).data
                try:
                    horarios: DiasFixos = DiasFixos.objects.filter(turma_idturma=turma)
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
                turma = Turma.objects.get(idturma=data["idTurma"])
                scheduleReceived: list = data['schedules']
                for i in scheduleReceived:
                    if i.__contains__('id'):
                        if i['id']:
                            if i['id'] > 0:
                                # Editando
                                dia = DiasFixos.objects.get(iddias_fixos=i['id'], turma_idturma=turma.idturma)
                                if i['horario'] is not None:
                                    newTime = dateutil.parser.parse(i['horario'])
                                    date1 = datetime(dia.horario.year, dia.horario.month, dia.horario.day,
                                                     dia.horario.hour,
                                                     dia.horario.minute)
                                    date2 = datetime(newTime.year, newTime.month, newTime.day, newTime.hour,
                                                     newTime.minute)
                                    if date1 != date2 or dia.sala != i['sala']:
                                        aulas = Aula.objects.filter(turma_idturma=turma,
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
                                turma_idturma=turma,
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


class SugestaoTurmaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SugestaoTurma.objects.all()
    serializer_class = SugestaoTurmaSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        try:
            sug = SugestaoTurma.objects.filter(turma_idturma_id=kwargs['pk'])
            return Response({"status": True,'suguestoes':self.serializer_class(sug).data})
        except Exception as ex:
            return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pupils_list(request: Request, id: int):
    try:
        aluno_turmaList = AlunoHasTurma()
        try:
            aluno_turmaList = AlunoHasTurma.objects.get(turma_idturma=id)
        except ObjectDoesNotExist as ex:
            print(">>> Wasn't Possible find the Turma")
            return Response({"status": False, "message": "Não foi possivel achar a turma"})
        alunos = Aluno.objects.filter(idaluno=aluno_turmaList.aluno_idaluno.idaluno)
        return Response({"status": True, "alunos": AlunoSerializer(alunos, many=True).data})
    except Exception as ex:
        return generic_except(ex)


def checkTimeForOpenClass():
    diferenca = timezone('America/Sao_Paulo')
    querry = Aula.objects.all()
    today = datetime.now().astimezone(diferenca)
    print(today.strftime("%H:%M:%S"))
    aulas = querry.filter(dia_horario__year=today.year, dia_horario__month=today.month, dia_horario__day=today.day,
                          dia_horario__hour=today.hour, dia_horario__minute=today.minute)
    for i in aulas:
        i.is_aberta_class = True
        i.save()
    print("--- checked Class Open")


set_interval(checkTimeForOpenClass, 60)
