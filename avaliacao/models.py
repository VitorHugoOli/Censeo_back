from django.db import models

# Create your models here.
from aluno.models import Aluno
from aula.models import Aula


class Avaliacao(models.Model):
    end_time = models.CharField(max_length=45, blank=True, null=True)
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Avaliacao'
        unique_together = (('id', 'aula', 'aluno'),)

    def __str__(self):
        return self.aula.turma.codigo + self.aula.dia_horario.__str__() + self.aluno.user.nome


class Caracteristica(models.Model):
    qualificacao = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Caracteristica'

    def __str__(self):
        return self.qualificacao


class Pergunta(models.Model):
    questao = models.CharField(max_length=45, blank=True, null=True)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True)
    caracteristica = models.ForeignKey(Caracteristica, models.CASCADE,
                                       db_column='Caracteristica_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pergunta'

    def __str__(self):
        return self.tipo_aula + " : " + self.questao


class Resposta(models.Model):
    aberta = models.IntegerField(blank=True, null=True)
    resposta = models.CharField(max_length=4, blank=True, null=True)
    resposta_aberta = models.CharField(max_length=45, blank=True, null=True)
    avaliacao = models.ForeignKey(Avaliacao, models.CASCADE, db_column='Avaliacao_id')
    avaliacao_aula = models.ForeignKey(Aula, models.CASCADE, db_column='Avaliacao_Aula_id')
    avaliacao_aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Avaliacao_Aluno_id')
    pergunta = models.ForeignKey(Pergunta, models.CASCADE, db_column='Pergunta_id')

    class Meta:
        managed = False
        db_table = 'Resposta'
        unique_together = (('id', 'pergunta'),)

    def __str__(self):
        return "Resposta"
