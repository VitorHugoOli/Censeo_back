from django.db import models

# Create your models here.
from aluno.models import Aluno
from aula.models import Aula


class Avaliacao(models.Model):
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.
    end_time = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Avaliacao'
        unique_together = (('id', 'aluno_idaluno', 'aula_idaula'),)

    def __str__(self):
        return self.aula_idaula.turma_idturma.codigo + self.aula_idaula.dia_horario.__str__() + self.aluno_idaluno.user_iduser.nome


class Caracteristica(models.Model):
    idcaracteristica = models.AutoField(db_column='idCaracteristica', primary_key=True)  # Field name made lowercase.
    qualificacao = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.qualificacao

    class Meta:
        managed = False
        db_table = 'Caracteristica'


class Pergunta(models.Model):
    idperguntas = models.AutoField(db_column='idPerguntas', primary_key=True)  # Field name made lowercase.
    questao = models.CharField(max_length=45, blank=True, null=True)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True)
    caracteristica_idcaracteristica = models.ForeignKey(Caracteristica, models.DO_NOTHING,
                                                        db_column='Caracteristica_idCaracteristica', blank=True,
                                                        null=True)  # Field name made lowercase.

    def __str__(self):
        return self.tipo_aula + " : " + self.questao

    class Meta:
        managed = False
        db_table = 'Pergunta'


class Resposta(models.Model):
    idrespostas = models.AutoField(db_column='idRespostas', primary_key=True)  # Field name made lowercase.
    aberta = models.IntegerField(blank=True, null=True)
    resposta = models.CharField(max_length=4, blank=True, null=True)
    resposta_aberta = models.CharField(max_length=45, blank=True, null=True)
    perguntas_idperguntas = models.ForeignKey(Pergunta, models.DO_NOTHING,
                                              db_column='Perguntas_idPerguntas')  # Field name made lowercase.
    avaliacao = models.ForeignKey(Avaliacao, models.DO_NOTHING, db_column='Avaliacao_id',
                                  related_name="Avaliacao_id")  # Field name made lowercase.
    avaliacao_aluno_idaluno = models.ForeignKey(Avaliacao, models.DO_NOTHING,
                                                db_column='Avaliacao_Aluno_idAluno',
                                                related_name='Avaliacao_Aluno_idAluno')  # Field name made lowercase.
    avaliacao_aula_idaula = models.ForeignKey(Avaliacao, models.DO_NOTHING,
                                              db_column='Avaliacao_Aula_idAula',
                                              related_name='Avaliacao_Aula_idAula')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Resposta'
        unique_together = (('idrespostas', 'perguntas_idperguntas'),)

    def __str__(self):
        return "Resposta"
