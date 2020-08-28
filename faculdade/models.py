from django.db import models


# Create your models here.

class Faculdade(models.Model):
    nome = models.CharField(max_length=45)
    sigla = models.CharField(max_length=45, blank=True, null=True)
    periodo_start = models.DateTimeField()
    periodo_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Faculdade'
