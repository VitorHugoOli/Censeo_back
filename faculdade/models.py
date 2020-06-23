from django.db import models

# Create your models here.
from aluno.models import Aluno


class TopicoFaculdade(models.Model):
    idtopico_faculdade = models.AutoField(db_column='idTopico_Faculdade',
                                          primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Topico_Faculdade'


class SugestaoFaculdade(models.Model):
    idsugestao_faculdade = models.AutoField(db_column='idSugestao_Faculdade',
                                            primary_key=True)  # Field name made lowercase.
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True)
    topico_faculdade_idtopico_faculdade = models.ForeignKey('TopicoFaculdade', models.DO_NOTHING,
                                                            db_column='Topico_Faculdade_idTopico_Faculdade')  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sugestao_Faculdade'
        unique_together = (('idsugestao_faculdade', 'topico_faculdade_idtopico_faculdade', 'aluno_idaluno'),)
