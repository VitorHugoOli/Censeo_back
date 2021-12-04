from datetime import datetime

from django.core.management.base import BaseCommand, CommandError

from aluno.models import Aluno
from avaliacao.models import Caracteristica, Pergunta
from curso.models import Curso, Disciplina
from faculdade.models import Faculdade
import pandas as pd

from professor.models import Professor
from turma.models import Turma, ProfessorHasTurma, DiasFixos, AlunoHasTurma
from user.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            facu = initFacu()
            initProfs()
            curso = initCursos(facu)
            initDisciplina(curso)
            init_turmas()
            init_prof_has_turma()
            init_fixed_days()
            init_alunos(curso)
            init_quiz()
            print("BD POPULADO COM SUCESSO")
        except Exception as ex:
            print(ex)
            print("Houve algum erro ao inicializar os dados no banco!")


def initFacu():
    try:
        facu = Faculdade.objects.get_or_create(nome="Universidade Federal de Viçosa -  Florestal", sigla="UFV", periodo_start="2021-12-06 03:33:44",
                                               periodo_end="2021-12-22 23:34:17")
        print("Faculdade criada com sucesso \\o/")
        return facu[0]
    except Exception as ex:
        raise Exception("xHouve algum erro ao inicializar a faculdade!\n" + repr(ex))


def initProfs():
    try:
        profs = [["daniel", "0001", "danielmendes@ufv.br"], ["glaucia", "0002", "glaucia@ufv.br"], ["thais", "0003", "thais.braga@ufv.br"]]
        for nome, matricula, email in profs:
            user = User.objects.get_or_create(nome=nome, matricula=matricula, email=email)[0]
            user.tipo_user = 1
            user.set_password("abc45678")
            user.save()
            Professor.objects.get_or_create(user=user)
    except Exception as ex:
        raise Exception("xHouve algum erro ao criar os professores!\n" + repr(ex))


def initCursos(facu):
    try:
        prof = Professor.objects.get(user__matricula="0001")
        curso = Curso.objects.get_or_create(nome="Ciência da Computação", codigo="CCF", professor_coordenador=prof, faculdade=facu)
        print("Curso criado com sucesso \\o/")
        return curso[0]
    except Exception as ex:
        raise Exception("xHouve algum erro ao inicializar o Curso!\n" + repr(ex))


def initDisciplina(curso):
    try:
        disciplinas = [["Banco de Dados".upper(), "CCF221", "BD"],
                       ["Engenharia de Software II".upper(), "CCF322", "ESOF II"],
                       ["Algoritmos e Estrutura de Dados I".upper(), "CCF211", "AEDS I"], ]
        for nome, codigo, sigla in disciplinas:
            Disciplina.objects.get_or_create(nome=nome, codigo=codigo, sigla=sigla, curso=curso)
        print("Disciplinas criadas com sucesso \\o/")
    except Exception as ex:
        raise ("xHouve algum erro ao inicializar as disciplinas!\n" + repr(ex))


def init_turmas():
    try:
        turmas = ["CCF221", "CCF322", "CCF211"]
        for i in turmas:
            disc = Disciplina.objects.get(codigo=i)
            Turma.objects.get_or_create(codigo=i, ano=2021, semestre=3, disciplina=disc)
        print("Turmas criadas com sucesso \\o/")
    except Exception as ex:
        raise Exception("xHouve algum erro ao inicializar as turmas!\n" + repr(ex))


def init_prof_has_turma():
    try:
        prof_turmas = [["0001", "CCF221"], ["0002", "CCF322"], ["0003", "CCF211"]]
        for m, c in prof_turmas:
            prof = Professor.objects.get(user__matricula=m)
            turma = Turma.objects.get(codigo=c)
            ProfessorHasTurma.objects.get_or_create(professor=prof, turma=turma)
        print("Prof_Turmas criado com sucesso \\o/")
    except Exception as ex:
        raise Exception("xHouve algum erro relacionar os professores a suas turmas!\n" + repr(ex))


def init_fixed_days():
    try:
        day_fixed = {"CCF221": [['SEG', '2020-12-06 09:50:00', 'REMOTA', '1', False], ['QUA', '2020-12-06 12:50:00', 'REMOTA', '1', False]],
                     "CCF322": [['SEG', '2020-12-06 12:50:00', 'REMOTA', '1', False], ['QUA', '2020-12-06 14:50:00', 'REMOTA', '1', False]],
                     "CCF211": [['TER', '2020-12-06 09:50:00', 'REMOTA', '1', False], ['QUI', '2020-12-06 09:50:00', 'REMOTA', '1', False]]}
        for i, days in day_fixed.items():
            turma = Turma.objects.get(codigo=i)
            for dia, horario, sala, to_end, is_async in days:
                dias = DiasFixos.objects.get_or_create(dia=dia, horario=datetime.strptime(horario, "%Y-%m-%d %H:%M:%S"), sala=sala, days_to_end=to_end, is_assincrona=is_async,
                                                       turma=turma)[0]
                # Todo: Precisa do save ?
                # dias.save()
        print("Dias_fixos criado com sucesso \\o/")
    except Exception as ex:
        raise Exception("xHouve algum erro ao criar os horarios fixos das turmas!\n" + repr(ex))


def init_alunos(curso):
    try:
        init_path = "../Dados_mock/"
        turmas = ["CCF131.csv", "CCF212.csv", "CCF355.csv"]

        for i in turmas:
            data = pd.read_csv(init_path + i)
            turma = Turma.objects.get(codigo=i.split(".csv")[0])
            for index, j in data.iterrows():
                user = User.objects.get_or_create(matricula=j['Matrícula'], nome=j['Nome'], email=j['E-mail'])[0]
                aluno = Aluno.objects.get_or_create(curso_idcurso=curso, user=user)[0]
                AlunoHasTurma.objects.get_or_create(aluno=aluno, turma=turma)
        print("Alunos criados com sucesso \\o/")
    except Exception as ex:
        raise Exception("xHouve algum erro ao criar os alunos!\n" + repr(ex))


def init_quiz():
    try:
        data = pd.read_csv("../Dados/quiz.csv", index_col="Conceito")
        for i in data.index.drop_duplicates():
            fator = Caracteristica.objects.get_or_create(qualificacao=i)[0]
            for j, d in data.loc[i].iterrows():
                Pergunta.objects.get_or_create(questao=d["Pergunta"], tipo_questao=2, tipo_aula='teorica', caracteristica=fator)
        print("Questionario criado com sucesso \\o/")
    except Exception as ex:
        raise Exception("xHouve algum erro ao criar os questionarios!\n" + repr(ex))
