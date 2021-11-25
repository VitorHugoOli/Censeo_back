from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

from Utils.Enums import tipo_relevancia, tipo_dias
from aluno.models import Aluno
from curso.models import Disciplina
from professor.models import Professor


# Create your models here.


class Turma(models.Model):
    codigo = models.CharField(max_length=45, blank=True, null=True)
    ano = models.CharField(max_length=45, blank=True, null=True)
    semestre = models.CharField(max_length=45, blank=True, null=True)
    disciplina = models.ForeignKey(Disciplina, models.CASCADE,
                                   db_column='Disciplina_id')

    class Meta:
        managed = False
        db_table = 'Turma'

    def __str__(self):
        return self.disciplina.nome + " " + self.codigo + " " + self.ano + " " + self.semestre


class DiasFixos(models.Model):
    TIPO_DIA = tipo_dias

    dia = models.CharField(max_length=3, blank=True, null=True, choices=TIPO_DIA)
    horario = models.DateTimeField(blank=True, null=True)
    sala = models.CharField(max_length=45, blank=True, null=True)
    days_to_end = models.IntegerField(blank=True, null=True)
    is_assincrona = models.BooleanField(default=0)
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='Turma_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Dias_Fixos'
        unique_together = (('id', 'turma'),)

    def __str__(self):
        return self.turma.codigo + " " + self.dia + " " + self.horario.__str__()

    def NormalDayToTipoDia(dia):
        if dia == "Segunda":
            return "SEG"
        if dia == "Terca":
            return "TER"
        if dia == "Quarta":
            return "QUA"
        if dia == "Quinta":
            return "QUI"
        if dia == "Sexta":
            return "SEX"
        if dia == "Sabado":
            return "SAB"

    def save(self, edit=False, *args, **kwargs):
        super().save(*args, **kwargs)
        if not edit:
            from aula.views import create_aulas
            create_aulas(self)


class TopicaTurma(models.Model):
    topico = models.CharField(max_length=45, blank=True, null=True)
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='Turma_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Topica_Turma'
        unique_together = (('id', 'turma'),)

    def __str__(self):
        return self.topico


class SugestaoTurma(models.Model):
    TIPO_RELEVANCIA = tipo_relevancia

    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True, choices=tipo_relevancia)
    data = models.DateTimeField()
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.
    topico = models.ForeignKey(TopicaTurma, models.CASCADE,
                               db_column='Topica_Turma_id')  # Field name made lowercase.
    turma = models.ForeignKey(Turma, models.CASCADE,
                              db_column='Topica_Turma_Turma_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sugestao_Turma'
        unique_together = (('id', 'aluno', 'topico', 'turma'),)

    def __str__(self):
        return self.aluno.user.nome + "   Titulo:" + self.titulo


class ProfessorHasTurma(models.Model):
    professor = models.ForeignKey(Professor, models.CASCADE, db_column='Professor_id')  # Field name made lowercase.
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='Turma_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor_has_Turma'
        unique_together = (('professor', 'turma'),)

    def __str__(self):
        return self.professor.user.nome + " " + self.turma.codigo


class AlunoHasTurma(models.Model):
    aluno = models.ForeignKey(Aluno, models.CASCADE, db_column='Aluno_id')  # Field name made lowercase.
    turma = models.ForeignKey(Turma, models.CASCADE, db_column='Turma_id')  # Field name made lowercase.
    xp = models.DecimalField(db_column='XP', max_digits=20, decimal_places=0, default=0)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Aluno_has_Turma'
        unique_together = (('aluno', 'turma'),)

    def __str__(self):
        return self.aluno.user.matricula + " " + self.turma.codigo


@receiver(pre_delete, sender=DiasFixos)
def delete_image_hook(sender, instance, using, **kwargs):
    turma = Turma.objects.get(id=instance.turma.id)
    from aula.models import Aula
    aulas = Aula.objects.filter(turma=turma, dia_horario__hour=instance.horario.hour,
                                dia_horario__minute=instance.horario.minute)
    for i in aulas:
        i.delete()
