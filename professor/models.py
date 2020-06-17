from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Professor(models.Model):
    idprofessor = models.IntegerField(db_column='idProfessor', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    login = models.CharField(max_length=45, blank=True, null=True)
    senha = models.CharField(max_length=45)
    lattes = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = False
        db_table = 'Professor'



