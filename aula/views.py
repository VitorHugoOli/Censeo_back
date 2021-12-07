# Create your views here.
import json
import timeit
import traceback
from datetime import timedelta, datetime

import dateutil.parser
import unidecode as unidecode
from django.db.models import Count, QuerySet, Q
from pytz import timezone
from rest_framework import viewsets, permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from Utils.CalcPeriodos import dayToNumber
from Utils.Except import generic_except
from aluno.models import Aluno
from aula.models import Aula, Prova, Teorica, Excursao, TrabalhoPratico
from aula.serializers import AulaSerializer
from avaliacao.models import Avaliacao
from professor.models import Professor
from turma.models import DiasFixos, ProfessorHasTurma, Turma, AlunoHasTurma
from user.models import User


class AulaViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = DiasFixos.objects.all()
    serializer_class = AulaSerializer
    permission_classes = [permissions.IsAuthenticated]
    TYPE_OBJ = {
        'teorica': Teorica,
        'prova': Prova,
        'trabalho': TrabalhoPratico,
        'excursao': Excursao
    }

    @staticmethod
    def createTypeObj(aula, extra, tipo):
        type_build = {
            'teorica': Teorica(aula=aula).save,
            'prova': Prova(aula=aula, quant_questao=extra).save,
            'trabalho': TrabalhoPratico(aula=aula, quant_membros_grupo=extra).save,
            'excursao': Excursao(aula=aula, nome_local=extra).save
        }
        type_build[tipo]()

    @staticmethod
    def checkExtra(aula, extra, tipo):
        if tipo == 'prova':
            prv = Prova.objects.get(aula=aula)
            if prv.quant_questao != extra:
                prv.quant_questao = extra
                prv.save()
        if tipo == 'trabalho':
            obj = TrabalhoPratico.objects.get(aula=aula)
            if obj.quant_membros_grupo != extra:
                obj.quant_membros_grupo = extra
                obj.save()
        if tipo == 'excursao':
            obj = Excursao.objects.get(aula=aula)
            if obj.nome_local != extra:
                obj.nome_local = extra
                obj.save()

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:
            if data.__contains__('turmaId'):
                turma = Turma.objects.get(id=data['turmaId'])
                aula = Aula(
                    dia_horario=dateutil.parser.parse(data['time']),
                    sala=data['room'],
                    is_aberta_class=0,
                    is_aberta_avaliacao=0,
                    turma=turma
                )
                aula.save()
                return Response({'status': True, 'aula': AulaSerializer(aula).data})
            else:
                return Response({'status': False, 'error': 'Something is missing 👀'})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            id_aula = kwargs['pk']
            data: dict = request.data
            aula = Aula.objects.get(id=id_aula)
            if data.__contains__('tipo') and data['tipo'] is not None:
                tipo = unidecode.unidecode(data['tipo'].lower())
            else:
                tipo = None

            aula_tipo = unidecode.unidecode(aula.tipo_aula.lower() if aula.tipo_aula is not None else '')

            if aula.tipo_aula != tipo:
                if aula.tipo_aula is not None:
                    self.TYPE_OBJ[aula_tipo].objects.get(aula=aula).delete()
                aula.tipo_aula = tipo
                self.createTypeObj(aula, data['extra'], tipo)
            elif aula.tipo_aula is not None:
                self.checkExtra(aula, data['extra'], tipo)

            aula.tema = data['tema']
            aula.is_assincrona = data['is_assincrona']
            aula.descricao = data['descricao']
            aula.link_documento = data['link']
            if aula.is_assincrona:
                aula.end_time = dateutil.parser.parse(data['end_time'])
            aula.save()
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)

    def destroy(self, request: Request, *args, **kwargs):
        try:
            id_aula = kwargs['pk']
            aula = Aula.objects.get(id=id_aula)
            if aula.tipo_aula == 'teorica':
                Teorica.objects.get(aula=aula).delete()
            elif aula.tipo_aula == 'prova':
                Prova.objects.get(aula=aula).delete()
            elif aula.tipo_aula == 'trabalho':
                TrabalhoPratico.objects.get(aula=aula).delete()
            elif aula.tipo_aula == 'excursao':
                Excursao.objects.get(aula=aula).delete()
            aula.delete()
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def retrieve_aula_from_turma(request: Request, id: int):
    type_obj = {
        'teorica': Teorica,
        'prova': Prova,
        'trabalho': TrabalhoPratico,
        'excursao': Excursao
    }

    aulas = None

    if (request.query_params.__contains__('is_end')):
        aulas = Aula.objects.filter(turma__id=id, end_time__isnull=False).order_by('-end_time')
    else:
        aulas = Aula.objects.filter(turma__id=id)

    dict_aulas = AulaSerializer(aulas, many=True).data
    aulas_json = json.loads(json.dumps(dict_aulas))

    for i in aulas_json:
        tipo = i['tipo_aula']
        if (tipo is not None or tipo != 'teorica') and (type_obj.__contains__(tipo)):
            try:
                obj = type_obj[tipo].objects.get(aula_id=i['id'])
                i['extra'] = obj.toDict()
            except Exception as ex:
                print(ex)

    return Response({"status": True, "aulas": aulas_json})


def create_aulas(dias_fixos: DiasFixos):
    '''
    this function creates all the class of an specify diaFixo model
    :param dias_fixos:
    :return:
    '''
    try:
        periodo_start = dias_fixos.turma.disciplina.curso.faculdade.periodo_start
        periodo_end = dias_fixos.turma.disciplina.curso.faculdade.periodo_end
        dayNumber = dayToNumber(dias_fixos.dia)
        if dayNumber != -1:
            delta = periodo_end - periodo_start
            for i in range(0, delta.days + 1, 1):
                day = periodo_start + timedelta(days=i)
                if day.weekday() == dayNumber:
                    aula = Aula(
                        dia_horario=datetime(day.year, day.month, day.day, dias_fixos.horario.hour,
                                             dias_fixos.horario.minute),
                        is_aberta_class=0,
                        is_aberta_avaliacao=0,
                        is_assincrona=dias_fixos.is_assincrona,
                        sala=dias_fixos.sala,
                        turma=dias_fixos.turma
                    )
                    if dias_fixos.is_assincrona:
                        aula.end_time = aula.dia_horario + timedelta(days=dias_fixos.days_to_end)
                    aula.save()
        else:
            raise Exception("Sorry, but the day passed is incorrect day: " + dias_fixos.dia.__str__())
    except Exception as ex:
        traceback.print_exc()
        print(ex)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def put_class_end(request):
    try:
        aula = Aula.objects.get(id=request.data['id'])
        aula.is_aberta_avaliacao = True
        aula.is_aberta_class = False
        diferenca = timezone('America/Sao_Paulo')
        aula.end_time = datetime.now().astimezone(diferenca)
        aula.save()
        return Response({'status': True})
    except Exception as ex:
        return generic_except(ex)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_professor_class_open(request):
    context = {"aulas": []}

    serializer_context = {
        'request': request,
    }

    aulas = Aula.objects.filter(turma__professorhasturma__professor__user=request.user, is_aberta_class=True, is_assincrona=False).order_by('dia_horario')
    context['aulas'] = AulaSerializer(aulas, many=True, context=serializer_context).data
    return Response({'status': True, **context})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_aluno_class_open(request):
    try:
        context = {}

        aulas: QuerySet[Aula] = Aula.objects.filter(turma__alunohasturma__aluno__user=request.user, is_aberta_class=False, is_aberta_avaliacao=True).filter(
            Q(avaliacao__completa=False) | Q(avaliacao__completa=None))

        context['aulas'] = AulaSerializer(aulas, many=True).data

        return Response({'status': True, **context})
    except Exception as ex:
        print(ex.args)
