from django.contrib import admin

# Register your models here.
from curso.models import *

admin.site.register(Curso)
admin.site.register(Disciplina)
admin.site.register(TopicoSugestaoCurso)
