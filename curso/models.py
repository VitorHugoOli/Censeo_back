from django.db import models

# Create your models here.
from professor.models import Professor


class Curso(models.Model):
    idcurso = models.AutoField(db_column='idCurso', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45, blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    professor_cordenador = models.ForeignKey(Professor, models.DO_NOTHING, db_column='Professor_cordenador',
                                             blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.nome+" "+self.codigo

    class Meta:
        managed = False
        db_table = 'Curso'


class Disciplina(models.Model):
    iddisciplina = models.AutoField(db_column='idDisciplina', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(max_length=45)
    nome = models.CharField(max_length=45)
    sigla = models.CharField(max_length=45)
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso_idCurso')  # Field name made lowercase.

    def __str__(self):
        return self.codigo

    class Meta:
        managed = False
        db_table = 'Disciplina'

class TopicoSugestaoCurso(models.Model):
    idtopico_sugestao_curso = models.AutoField(db_column='idTopico_Sugestao_Curso',
                                               primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.topico

    class Meta:
        managed = False
        db_table = 'Topico_Sugestao_Curso'






