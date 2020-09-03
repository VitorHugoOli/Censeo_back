from django.db import models

# Create your models here.
from user.models import User


class Professor(models.Model):
    lattes = models.CharField(max_length=45, blank=True, null=True)
    user = models.ForeignKey(User, models.CASCADE, db_column='User_id')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Professor'
        unique_together = (('id', 'user'),)

    def __str__(self):
        return "Professor " + self.user.nome