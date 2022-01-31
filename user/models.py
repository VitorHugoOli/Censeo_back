import unicodedata

from django.contrib.auth import password_validation
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import (
    check_password, is_password_usable, make_password,
)
from django.db import models
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.crypto import salted_hmac
from rest_framework.authtoken.models import Token

from censeo import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, nome, email, username, matricula, password):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not matricula:
            raise ValueError('Users must have an matricula')

        user = self.model(
            nome=nome,
            email=self.normalize_email(email) if email is not None else email,
            username=username,
            matricula=matricula,
            tipo_user=2,
            is_admin=1
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nome, email, username, matricula, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            nome,
            email,
            username,
            matricula,
            password=password
        )
        user.save(using=self._db)
        return user


class User(models.Model):
    TIPOUSER = (('Professor', 'Professor'),
                ('Aluno', 'Aluno'))

    nome = models.CharField(max_length=45, blank=True, null=True)
    username = models.CharField(unique=True, max_length=45, blank=True, null=True)
    matricula = models.CharField(unique=True, max_length=45)
    email = models.CharField(unique=True, max_length=45, null=True)
    password = models.CharField(unique=True, max_length=125)
    tipo_user = models.CharField(max_length=9, choices=TIPOUSER, default='Aluno')
    push_token = models.CharField(unique=True, max_length=200)
    first_time = models.BooleanField(default=1)
    is_admin = models.BooleanField(default=0)

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'matricula'
    REQUIRED_FIELDS = ['nome', 'email', 'username']

    is_active = True

    objects = CustomUserManager()

    class Meta:
        managed = False
        db_table = 'User'

    def __str__(self):
        return self.get_username()

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    token = None

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    @staticmethod
    def has_perm(perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def has_module_perms(app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
            _token = Token.objects.create(user=instance)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self._password is not None:
            password_validation.password_changed(self._password, self)
            self._password = None

    def get_username(self):
        """Return the username for this User."""
        return getattr(self, self.USERNAME_FIELD)

    def clean(self):
        setattr(self, self.USERNAME_FIELD, self.normalize_username(self.get_username()))

    def natural_key(self):
        return (self.get_username(),)

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def set_password(self, raw_password):
        self.password = make_password(raw_password)
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

    def set_unusable_password(self):
        # Set a value that will never be a valid hash
        self.password = make_password(None)

    def has_usable_password(self):
        """
        Return False if set_unusable_password() has been called for this user.
        """
        return is_password_usable(self.password)

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "django.contrib.auth.models.AbstractBaseUser.get_session_auth_hash"
        return salted_hmac(key_salt, self.password).hexdigest()

    @classmethod
    def get_email_field_name(cls):
        try:
            return cls.EMAIL_FIELD
        except AttributeError:
            return 'email'

    @classmethod
    def normalize_username(cls, username):
        return unicodedata.normalize('NFKC', username) if isinstance(username, str) else username

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = email_name + '@' + domain_part.lower()
        return email
