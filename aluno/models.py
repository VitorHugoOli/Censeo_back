from django.db import models

# Create your models here.
from curso.models import Curso
from user.models import User


class Aluno(models.Model):
    idaluno = models.AutoField(db_column='idAluno', primary_key=True)  # Field name made lowercase.
    xp = models.DecimalField(db_column='XP', max_digits=20, decimal_places=0, blank=True,
                             null=True)  # Field name made lowercase.
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING,
                                      db_column='Curso_idCurso')  # Field name made lowercase.
    user_iduser = models.ForeignKey(User, models.DO_NOTHING, db_column='User_idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aluno'
        unique_together = (('idaluno', 'user_iduser'),)


class Elo(models.Model):
    idelo = models.AutoField(db_column='idElo', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return self.aluno_idaluno.matricula + " " + self.tipo

    class Meta:
        managed = False
        db_table = 'Elo'
        unique_together = (('idelo', 'aluno_idaluno'),)


class TopicoSugestaoCurso(models.Model):
    idtopico_sugestao_curso = models.AutoField(db_column='idTopico_Sugestao_Curso',
                                               primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.topico

    class Meta:
        managed = False
        db_table = 'Topico_Sugestao_Curso'


class SugestaoCurso(models.Model):
    idsugestao_curso = models.AutoField(db_column='idSugestao_Curso', primary_key=True)  # Field name made lowercase.
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True)
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso_idCurso')  # Field name made lowercase.
    topico_sugestao_curso_idtopico_sugestao_curso = models.ForeignKey(TopicoSugestaoCurso, models.DO_NOTHING,
                                                                      db_column='Topico_Sugestao_Curso_idTopico_Sugestao_Curso')  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return "titulo: " + self.titulo

    class Meta:
        managed = False
        db_table = 'Sugestao_Curso'
        unique_together = (
            ('idsugestao_curso', 'curso_idcurso', 'topico_sugestao_curso_idtopico_sugestao_curso', 'aluno_idaluno'),)
