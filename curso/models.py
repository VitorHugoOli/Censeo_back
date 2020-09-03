from django.db import models

# Create your models here.
from faculdade.models import Faculdade
from professor.models import Professor


class Curso(models.Model):
    nome = models.CharField(max_length=45, blank=True, null=True)
    codigo = models.CharField(max_length=45, blank=True, null=True)
    professor_coordenador = models.ForeignKey(Professor, models.SET_NULL, db_column='Professor_coordenador',
                                              blank=True, null=True)
    faculdade = models.ForeignKey(Faculdade, models.CASCADE, db_column='Faculdade_id')

    class Meta:
        managed = False
        db_table = 'Curso'

    def __str__(self):
        return self.nome + " " + self.codigo


class Disciplina(models.Model):
    codigo = models.CharField(max_length=45)
    nome = models.CharField(max_length=45)
    sigla = models.CharField(max_length=45)
    curso = models.ForeignKey(Curso, models.CASCADE, db_column='Curso_id')

    class Meta:
        managed = False
        db_table = 'Disciplina'

    def __str__(self):
        return self.codigo
