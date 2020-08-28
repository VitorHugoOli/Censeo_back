from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from aluno.models import Aluno
from curso.models import Disciplina
from professor.models import Professor


# Create your models here.


class Turma(models.Model):
    idturma = models.AutoField(db_column='idTurma', primary_key=True)  # Field name made lowercase.
    codigo = models.CharField(max_length=45, blank=True, null=True)
    ano = models.CharField(max_length=45, blank=True, null=True)
    semestre = models.CharField(max_length=45, blank=True, null=True)
    disciplina_iddisciplina = models.ForeignKey(Disciplina, models.DO_NOTHING,
                                                db_column='Disciplina_idDisciplina')  # Field name made lowercase.

    def __str__(self):
        return self.disciplina_iddisciplina.nome + " " + self.codigo + " " + self.ano + " " + self.semestre

    class Meta:
        managed = False
        db_table = 'Turma'


class DiasFixos(models.Model):
    iddias_fixos = models.AutoField(db_column='idDias_Fixos', primary_key=True)  # Field name made lowercase.
    dia = models.CharField(max_length=3, blank=True, null=True)
    horario = models.DateTimeField(blank=True, null=True)
    sala = models.CharField(max_length=45, blank=True, null=True)
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    def __str__(self):
        return self.turma_idturma.codigo + " " + self.dia + " " + self.horario.__str__()

    def save(self, edit=False, *args, **kwargs):
        super().save(*args, **kwargs)
        if not edit:
            from aula.views import createAulas
            createAulas(self)

    class Meta:
        managed = False
        db_table = 'Dias_Fixos'
        unique_together = (('iddias_fixos', 'turma_idturma'),)


class TopicaTurma(models.Model):
    idtopica_turma = models.AutoField(db_column='idTopica_Turma', primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.topico

    class Meta:
        managed = False
        db_table = 'Topica_Turma'


class SugestaoTurma(models.Model):
    idsugestao_turma = models.AutoField(db_column='idSugestao_Turma', primary_key=True)  # Field name made lowercase.
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True)
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.
    topica_turma_idtopica_turma = models.ForeignKey(TopicaTurma, models.DO_NOTHING,
                                                    db_column='Topica_Turma_idTopica_Turma')  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return self.aluno_idaluno.nome + "   Titulo:" + self.titulo

    class Meta:
        managed = False
        db_table = 'Sugestao_Turma'
        unique_together = (('idsugestao_turma', 'turma_idturma', 'topica_turma_idtopica_turma', 'aluno_idaluno'),)


class ProfessorHasTurma(models.Model):
    professor_idprofessor = models.ForeignKey(Professor, models.DO_NOTHING,
                                              db_column='Professor_idProfessor')  # Field name made lowercase.
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor_has_Turma'
        unique_together = (('id', 'professor_idprofessor', 'turma_idturma'),)

    def __str__(self):
        return self.professor_idprofessor.user_iduser.nome + " " + self.turma_idturma.codigo


class AlunoHasTurma(models.Model):
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.
    turma_idturma = models.ForeignKey(Turma, models.DO_NOTHING,
                                      db_column='Turma_idTurma')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aluno_has_Turma'
        unique_together = (('id', 'aluno_idaluno', 'turma_idturma'),)

    def __str__(self):
        return self.aluno_idaluno.user_iduser.matricula + " " + self.turma_idturma.codigo


@receiver(pre_delete, sender=DiasFixos)
def delete_image_hook(sender, instance, using, **kwargs):
    turma = Turma.objects.get(idturma=instance.turma_idturma.idturma)
    from aula.models import Aula
    aulas = Aula.objects.filter(turma_idturma=turma, dia_horario__hour=instance.horario.hour,
                                dia_horario__minute=instance.horario.minute)
    for i in aulas:
        i.delete()
