from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password, make_password
from django.db import models

# Create your models here.
from curso.models import Curso


class Aluno(models.Model):
    idaluno = models.AutoField(db_column='idAluno', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(max_length=45, blank=True, null=True)
    matricula = models.CharField(unique=True, max_length=45)
    username = models.CharField(unique=True, max_length=45, blank=True, null=True)
    email = models.CharField(unique=True, max_length=45)
    senha = models.CharField(max_length=100)
    xp = models.DecimalField(db_column='XP', max_digits=20, decimal_places=0, blank=True,
                             null=True)  # Field name made lowercase.
    first_time = models.IntegerField(blank=True, null=True)
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING,
                                      db_column='Curso_idCurso')  # Field name made lowercase.

    # Stores the raw password if set_password() is called so that it can
    # be passed to password_changed() after the model is saved.
    _password = None

    def __str__(self):
        return self.nome + " " + self.matricula

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
            self.save(update_fields=["senha"])

        return check_password(raw_password, self.senha, setter)

    class Meta:
        managed = False
        db_table = 'Aluno'


class Elo(models.Model):
    idelo = models.AutoField(db_column='idElo', primary_key=True)  # Field name made lowercase.
    tipo = models.CharField(db_column='Tipo', max_length=7, blank=True, null=True)  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return self.aluno_idaluno.matricula + " " + self.tipo

    class Meta:
        managed = False
        db_table = 'Elo'
        unique_together = (('idelo', 'aluno_idaluno'),)


class TopicoSugestaoCurso(models.Model):
    idtopico_sugestao_curso = models.AutoField(db_column='idTopico_Sugestao_Curso',
                                               primary_key=True)  # Field name made lowercase.
    topico = models.CharField(max_length=45, blank=True, null=True)

    def __str__(self):
        return self.topico

    class Meta:
        managed = False
        db_table = 'Topico_Sugestao_Curso'


class SugestaoCurso(models.Model):
    idsugestao_curso = models.AutoField(db_column='idSugestao_Curso', primary_key=True)  # Field name made lowercase.
    sugestao = models.CharField(max_length=45, blank=True, null=True)
    titulo = models.CharField(max_length=45, blank=True, null=True)
    relevancia = models.CharField(max_length=15, blank=True, null=True)
    curso_idcurso = models.ForeignKey(Curso, models.DO_NOTHING, db_column='Curso_idCurso')  # Field name made lowercase.
    topico_sugestao_curso_idtopico_sugestao_curso = models.ForeignKey(TopicoSugestaoCurso, models.DO_NOTHING,
                                                                      db_column='Topico_Sugestao_Curso_idTopico_Sugestao_Curso')  # Field name made lowercase.
    aluno_idaluno = models.ForeignKey(Aluno, models.DO_NOTHING, db_column='Aluno_idAluno')  # Field name made lowercase.

    def __str__(self):
        return "titulo: " + self.titulo

    class Meta:
        managed = False
        db_table = 'Sugestao_Curso'
        unique_together = (
            ('idsugestao_curso', 'curso_idcurso', 'topico_sugestao_curso_idtopico_sugestao_curso', 'aluno_idaluno'),)
