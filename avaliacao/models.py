from django.db import models

from Utils.Enums import tipo_aula, tipo_resposta, tipo_questao_enum, tipo_qualificativo
# Create your models here.
from aluno.models import Aluno
from aula.models import Aula


class Avaliacao(models.Model):
    end_time = models.DateTimeField(blank=True, null=True)
    completa = models.BooleanField(null=False)
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.
    pontos = models.DecimalField(max_digits=20, decimal_places=0, blank=True,
                                 null=True)  # Field name made lowercase.

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
    TIPO_AULA = tipo_aula
    TIPO_QUESTAO = tipo_questao_enum

    questao = models.CharField(max_length=200, blank=True, null=True)
    tipo_questao = models.CharField(max_length=20, blank=True, null=True, choices=TIPO_QUESTAO)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True, choices=TIPO_AULA)

    caracteristica = models.ForeignKey(Caracteristica, models.CASCADE,
                                       db_column='Caracteristica_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Pergunta'

    def __str__(self):
        return self.tipo_aula + " : " + self.questao


class Resposta(models.Model):
    TIPO_QUALIFICATIVA = tipo_qualificativo
    TIPO_RESPOSTA = tipo_resposta

    tipo_resposta = models.CharField(max_length=20, choices=TIPO_RESPOSTA)
    resposta_binario = models.BooleanField(blank=True, null=True)
    resposta_qualificativa = models.CharField(max_length=45, blank=True, null=True, choices=TIPO_QUALIFICATIVA)
    resposta_aberta = models.CharField(max_length=45, blank=True, null=True)

    avaliacao = models.ForeignKey(Avaliacao, models.CASCADE, db_column='Avaliacao_id')
    avaliacao_aula = models.ForeignKey(Aula, models.CASCADE, db_column='Avaliacao_Aula_id')
    avaliacao_aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Avaliacao_Aluno_id')
    pergunta = models.ForeignKey(Pergunta, models.CASCADE, db_column='Pergunta_id')

    class Meta:
        managed = False
        db_table = 'Resposta'
        unique_together = (('avaliacao', 'pergunta'),)

    def __str__(self):
        return "Resposta"
