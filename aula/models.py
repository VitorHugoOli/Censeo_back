from django.db import models

# Create your models here.
from turma.models import Turma


class Aula(models.Model):
    idaula = models.IntegerField(db_column='idAula', primary_key=True)  # Field name made lowercase.
    dia_horario = models.DateTimeField(blank=True, null=True)
    tipo_aula = models.CharField(max_length=8, blank=True, null=True)
    tema = models.CharField(max_length=45, blank=True, null=True)
    descricao = models.CharField(max_length=45, blank=True, null=True)
    enttime = models.DateTimeField(db_column='entTime', blank=True, null=True)  # Field name made lowercase.
    is_aberta = models.IntegerField(blank=True, null=True)
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    def __str__(self):
        return self.turma_idturma.codigo + self.dia_horario.__str__()

    class Meta:
        managed = False
        db_table = 'Aula'


class Prova(models.Model):
    idprova = models.IntegerField(db_column='idProva', primary_key=True)  # Field name made lowercase.
    descricao_conteudo = models.CharField(max_length=45, blank=True, null=True)
    quant_questao = models.CharField(max_length=45, blank=True, null=True)
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.

    def __str__(self):
        return "Prova:" + self.aula_idaula.turma_idturma.codigo + self.aula_idaula.turma_idturma.ano + self.aula_idaula.turma_idturma.semestre + self.aula_idaula.dia_horario.__str__()

    class Meta:
        managed = False
        db_table = 'Prova'
        unique_together = (('idprova', 'aula_idaula'),)


class Teorica(models.Model):
    idteorica = models.IntegerField(db_column='idTeorica', primary_key=True)  # Field name made lowercase.
    conteudo = models.CharField(max_length=45, blank=True, null=True)
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.

    def __str__(self):
        return "Teorica:" + self.aula_idaula.turma_idturma.codigo + self.aula_idaula.turma_idturma.ano + self.aula_idaula.turma_idturma.semestre + self.aula_idaula.dia_horario.__str__()


    class Meta:
        managed = False
        db_table = 'Teorica'
        unique_together = (('idteorica', 'aula_idaula'),)


class TrabalhoPratico(models.Model):
    idtrabalho_pratico = models.IntegerField(db_column='idTrabalho_Pratico',
                                             primary_key=True)  # Field name made lowercase.
    link_documentacao = models.CharField(max_length=45, blank=True, null=True)
    quant_membros_grupo = models.CharField(max_length=45, blank=True, null=True)
    desenvolvimento_esperado = models.CharField(max_length=45, blank=True, null=True)
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.

    def __str__(self):
        return "TP:" + self.aula_idaula.turma_idturma.codigo + self.aula_idaula.turma_idturma.ano + self.aula_idaula.turma_idturma.semestre + self.aula_idaula.dia_horario.__str__()


    class Meta:
        managed = False
        db_table = 'Trabalho_Pratico'
        unique_together = (('idtrabalho_pratico', 'aula_idaula'),)


class Excursao(models.Model):
    idexcursao = models.IntegerField(db_column='idExcursao', primary_key=True)  # Field name made lowercase.
    nome_local = models.CharField(max_length=45, blank=True, null=True)
    objetivo = models.CharField(max_length=45, blank=True, null=True)
    atividade = models.CharField(max_length=45, blank=True, null=True)
    aula_idaula = models.ForeignKey(Aula, models.DO_NOTHING, db_column='Aula_idAula')  # Field name made lowercase.

    def __str__(self):
        return "Excurção:" + self.aula_idaula.turma_idturma.codigo + self.aula_idaula.turma_idturma.ano + self.aula_idaula.turma_idturma.semestre + self.aula_idaula.dia_horario.__str__()


    class Meta:
        managed = False
        db_table = 'Excursao'
        unique_together = (('idexcursao', 'aula_idaula'),)
