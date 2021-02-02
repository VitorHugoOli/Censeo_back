from django.db import models
from Utils.Enums import tipo_aula

# Create your models here.
from turma.models import Turma


class Aula(models.Model):
    TIPOAULA = tipo_aula

    dia_horario = models.DateTimeField()
    sala = models.CharField(max_length=45, blank=True, null=True)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True, choices=tipo_aula)
    tema = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)
    link_documento = models.CharField(max_length=45, blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    is_aberta_avaliacao = models.BooleanField(blank=True, null=True)
    is_aberta_class = models.BooleanField(blank=True, null=True)
    is_assincrona = models.BooleanField(default=0)
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='Turma_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aula'

    def __str__(self):
        return self.turma.codigo + " " + self.dia_horario.__str__()


class Prova(models.Model):
    quant_questao = models.CharField(max_length=45, blank=True, null=True)
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Prova'
        unique_together = (('id', 'aula'),)

    def __str__(self):
        return "Prova:" + self.aula.turma.codigo + self.aula.turma.ano + self.aula.turma.semestre + self.aula.dia_horario.__str__()

    def toDict(self):
        return {'id': self.id, 'quant_questao': self.quant_questao}


class Teorica(models.Model):
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Teorica'
        unique_together = (('id', 'aula'),)

    def __str__(self):
        return "Teorica:" + self.aula.turma.codigo + self.aula.turma.ano + self.aula.turma.semestre + self.aula.dia_horario.__str__()

    def toDict(self):
        return {'id': self.id}


class TrabalhoPratico(models.Model):
    quant_membros_grupo = models.CharField(max_length=45, blank=True, null=True)
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Trabalho_Pratico'
        unique_together = (('id', 'aula'),)

    def __str__(self):
        return "TP:" + self.aula.turma.codigo + self.aula.turma.ano + self.aula.turma.semestre + self.aula.dia_horario.__str__()

    def toDict(self):
        return {'id': self.id, 'quant_membros_grupo': self.quant_membros_grupo}


class Excursao(models.Model):
    nome_local = models.CharField(max_length=45, blank=True, null=True)
    aula = models.ForeignKey(Aula, models.CASCADE, db_column='Aula_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Excursao'
        unique_together = (('id', 'aula'),)

    def __str__(self):
        return "Excurção:" + self.aula.turma.codigo + self.aula.turma.ano + self.aula.turma.semestre + self.aula.dia_horario.__str__()

    def toDict(self):
        return {'id': self.id, 'nome_local': self.nome_local}
