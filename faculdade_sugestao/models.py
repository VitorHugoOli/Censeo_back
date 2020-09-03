from django.db import models

# Create your models here.
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
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=6, blank=True, null=True)
    topico_faculdade = models.ForeignKey(TopicoFaculdade, models.CASCADE,
                                         db_column='Topico_Faculdade_id')
    topico_faculdade_faculdade = models.ForeignKey(Faculdade, models.CASCADE,
                                                   db_column='Topico_Faculdade_Faculdade_id', related_name='faculdade')
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')
    aluno_user = models.ForeignKey(User, models.CASCADE, db_column='Aluno_User_id', related_name='user')

    class Meta:
        managed = False
        db_table = 'Sugestao_Faculdade'
        unique_together = (('id', 'topico_faculdade', 'topico_faculdade_faculdade', 'aluno', 'aluno_user'),)
