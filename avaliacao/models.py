from django.db import models


# Create your models here.
from aluno.models import Aluno
from aula.models import Aula


class Avaliacoes(models.Model):
    aluno_idaluno = models.OneToOneField(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno',
                                         primary_key=True)  # Field name made lowercase.
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.
    end_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.aula_idaula.turma_idturma.codigo + self.aula_idaula.dia_horario.__str__() + self.aluno_idaluno.nome


    class Meta:
        managed = False
        db_table = 'Avaliacoes'
        unique_together = (('aluno_idaluno', 'aula_idaula'),)

class Perguntas(models.Model):
    idperguntas = models.IntegerField(db_column='idPerguntas', primary_key=True)  # Field name made lowercase.
    questao = models.CharField(max_length=45, blank=True, null=True)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.tipo_aula +" : "+self.questao


    class Meta:
        managed = False
        db_table = 'Perguntas'

class Respostas(models.Model):
    idrespostas = models.IntegerField(db_column='idRespostas', primary_key=True)  # Field name made lowercase.
    aberta = models.IntegerField(blank=True, null=True)
    resposta = models.CharField(max_length=4, blank=True, null=True)
    resposta_aberta = models.CharField(max_length=45, blank=True, null=True)
    avaliacoes_aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING,
                                                 db_column='Avaliacoes_Aluno_idAluno')  # Field name made lowercase.
    avaliacoes_aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING,
                                               db_column='Avaliacoes_Aula_idAula')  # Field name made lowercase.
    perguntas_idperguntas = models.ForeignKey(Perguntas, models.DO_NOTHING,
                                              db_column='Perguntas_idPerguntas')  # Field name made lowercase.

    def __str__(self):
        return "Resposta "

    class Meta:
        managed = False
        db_table = 'Respostas'
        unique_together = (
        ('idrespostas', 'avaliacoes_aluno_idaluno', 'avaliacoes_aula_idaula', 'perguntas_idperguntas'),)





class Caracteristica(models.Model):
    idcaracteristica = models.IntegerField(db_column='idCaracteristica', primary_key=True)  # Field name made lowercase.
    qualificacao = models.CharField(max_length=45, blank=True, null=True)
    perguntas_idperguntas = models.ForeignKey(Perguntas, models.DO_NOTHING,
                                              db_column='Perguntas_idPerguntas')  # Field name made lowercase.

    def __str__(self):
        return self.qualificacao


    class Meta:
        managed = False
        db_table = 'Caracteristica'
