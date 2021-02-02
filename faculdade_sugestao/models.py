from django.db import models

# Create your models here.
from Utils.Enums import tipo_relevancia
from aluno.models import Aluno
from faculdade.models import Faculdade
from user.models import User


class TopicoFaculdade(models.Model):
    topico = models.CharField(max_length=45, blank=True, null=True)
    faculdade = models.ForeignKey(Faculdade, models.CASCADE, db_column='Faculdade_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Topico_Faculdade'
        unique_together = (('id', 'faculdade'),)


class SugestaoFaculdade(models.Model):
    TIPO_RELEVANCIA = tipo_relevancia

    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=6, blank=True, null=True, choices=tipo_relevancia)
    data = models.DateTimeField()
    topico = models.ForeignKey(TopicoFaculdade, models.CASCADE,
                               db_column='Topico_Faculdade_id')
    faculdade = models.ForeignKey(Faculdade, models.CASCADE,
                                  db_column='Topico_Faculdade_Faculdade_id', related_name='faculdade')
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')
    user = models.ForeignKey(User, models.CASCADE, db_column='Aluno_User_id', related_name='user')

    class Meta:
        managed = False
        db_table = 'Sugestao_Faculdade'
        unique_together = (('id', 'topico', 'faculdade', 'aluno', 'aluno'),)
