from django.db import models

# Create your models here.
from aluno.models import Aluno


class Avatar(models.Model):
    url = models.CharField(max_length=45)
    date = models.DateField(blank=True, null=True)
    is_shiny = models.BooleanField(default=False)

    class Meta:
        managed = False
        db_table = 'Avatar'


class AvatarHasAluno(models.Model):
    avatar = models.OneToOneField(Avatar, models.DO_NOTHING, db_column='Avatar_id',
                                  primary_key=True)  # Field name made lowercase.
    aluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Avatar_has_Aluno'
        unique_together = (('avatar', 'aluno'),)
