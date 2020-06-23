from django.contrib.auth import password_validation
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.db import models


# Create your models here.


class Professor(models.Model):
    idprofessor = models.AutoField(db_column='idProfessor', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45, blank=True, null=True)
    matricula = models.CharField(unique=True, max_length=45)
    username = models.CharField(unique=True, max_length=45, blank=True, null=True)
    email = models.CharField(unique=True, max_length=45)
    senha = models.CharField(max_length=100)
    lattes = models.CharField(max_length=45, blank=True, null=True)

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
        self._password = raw_password

    def check_password(self, raw_password):
        """
        Return a boolean of whether the raw_password was correct. Handles
        hashing formats behind the scenes.
        """
        def setter(raw_password):
            self.set_password(raw_password)
            # Password hash upgrades shouldn't be considered password changes.
            self._password = None
            self.save(update_fields=["password"])
        return check_password(raw_password, self.password, setter)

    class Meta:
        managed = False
        db_table = 'Professor'


