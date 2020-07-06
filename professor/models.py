from django.db import models


# Create your models here.
from user.models import User


class Professor(models.Model):
    idprofessor = models.AutoField(db_column='idProfessor', primary_key=True)  # Field name made lowercase.
    lattes = models.CharField(max_length=45, blank=True, null=True)
    user_iduser = models.ForeignKey(User, models.DO_NOTHING, db_column='User_idUser')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor'
        unique_together = (('idprofessor', 'user_iduser'),)
