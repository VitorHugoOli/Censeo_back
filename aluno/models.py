from django.db import models

# Create your models here.
from Utils.Enums import tipo_aula, tipo_relevancia, tipo_strike
from curso.models import Curso
from user.models import User


class Aluno(models.Model):
    xp = models.DecimalField(db_column='XP', max_digits=20, decimal_places=0, default=0)  # Field name made lowercase.
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING,
                                      db_column='Curso_idCurso')  # Field name made lowercase.
    user = models.ForeignKey(User, models.CASCADE, db_column='User_id')  # Field name made lowercase.

    def __str__(self):
        return self.user.nome + " " + self.user.matricula + " Aluno"

    class Meta:
        managed = False
        db_table = 'Aluno'
        unique_together = (('id', 'user'),)


class Elo(models.Model):
    tipo = models.CharField(db_column='Tipo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Elo'
        unique_together = (('id', 'aluno'),)


class TopicoSugestaoCurso(models.Model):
    topico = models.CharField(max_length=45, blank=True, null=True)
    curso = models.ForeignKey(Curso, models.CASCADE, db_column='Curso_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Topico_Sugestao_Curso'
        unique_together = (('id', 'curso'),)


class SugestaoCurso(models.Model):
    TIPO_RELEVANCIA = tipo_relevancia

    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True, choices=tipo_relevancia)
    data = models.DateTimeField()
    topico = models.ForeignKey(TopicoSugestaoCurso, models.CASCADE,
                                              db_column='Topico_Sugestao_Curso_id')  # Field name made lowercase.
    curso = models.ForeignKey(Curso, models.CASCADE,
                              db_column='Topico_Sugestao_Curso_Curso_id')  # Field name made lowercase.
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sugestao_Curso'
        unique_together = (('id', 'topico', 'curso', 'aluno'),)

    def __str__(self):
        return "titulo: " + self.titulo


class StrikeDia(models.Model):
    TIPO_STRIKE = tipo_strike

    strike = models.CharField(max_length=9, blank=True, null=True, choices=tipo_strike)
    date = models.DateField()
    aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Strike_Dia'
        unique_together = (('id', 'aluno'),)
