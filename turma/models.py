from django.db import models

# Create your models here.
from aluno.models import Aluno
from curso.models import Disciplina
from professor.models import Professor


class Turma(models.Model):
    idturma = models.IntegerField(db_column='idTurma', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45, blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    ano = models.CharField(max_length=45, blank=True, null=True)
    semestre = models.CharField(max_length=45, blank=True, null=True)
    disciplina_iddisciplina = models.ForeignKey(Disciplina, models.DO_NOTHING,
                                                db_column='Disciplina_idDisciplina')  # Field name made lowercase.

    def __str__(self):
        return self.nome+" "+self.codigo+" "+self.ano+" "+self.semestre

    class Meta:
        managed = False
        db_table = 'Turma'


class DiasFixos(models.Model):
    iddias_fixos = models.IntegerField(db_column='idDias_Fixos', primary_key=True)  # Field name made lowercase.
    dia = models.CharField(max_length=3, blank=True, null=True)
    horario = models.DateTimeField(blank=True, null=True)
    sala = models.CharField(max_length=45, blank=True, null=True)
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    def __str__(self):
        return self.turma_idturma.codigo+" "+self.dia+" "+self.horario.__str__()

    class Meta:
        managed = False
        db_table = 'Dias_Fixos'
        unique_together = (('iddias_fixos', 'turma_idturma'),)


class TopicaTurma(models.Model):
    idtopica_turma = models.IntegerField(db_column='idTopica_Turma', primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.topico

    class Meta:
        managed = False
        db_table = 'Topica_Turma'


class SugestaoTurma(models.Model):
    idsugestao_turma = models.IntegerField(db_column='idSugestao_Turma', primary_key=True)  # Field name made lowercase.
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True)
    sugestao_turmacol = models.CharField(db_column='Sugestao_Turmacol', max_length=45, blank=True,
                                         null=True)  # Field name made lowercase.
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.
    topica_turma_idtopica_turma = models.ForeignKey(TopicaTurma, models.DO_NOTHING,
                                                    db_column='Topica_Turma_idTopica_Turma')  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return self.aluno_idaluno.nome+"   Titulo:"+self.titulo

    class Meta:
        managed = False
        db_table = 'Sugestao_Turma'
        unique_together = (('idsugestao_turma', 'turma_idturma', 'topica_turma_idtopica_turma', 'aluno_idaluno'),)

class ProfessorHasTurma(models.Model):
    professor_idprofessor = models.OneToOneField(Professor, models.DO_NOTHING, db_column='Professor_idProfessor',
                                                 primary_key=True)  # Field name made lowercase.
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    def __str__(self):
        return self.professor_idprofessor.nome+" "+self.turma_idturma.codigo

    class Meta:
        managed = False
        db_table = 'Professor_has_Turma'
        unique_together = (('professor_idprofessor', 'turma_idturma'),)

class AlunoHasTurma(models.Model):
    aluno_idaluno = models.OneToOneField(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno',
                                         primary_key=True)  # Field name made lowercase.
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    def __str__(self):
        return self.aluno_idaluno.matricula+" "+self.turma_idturma.codigo

    class Meta:
        managed = False
        db_table = 'Aluno_has_Turma'
        unique_together = (('aluno_idaluno', 'turma_idturma'),)
