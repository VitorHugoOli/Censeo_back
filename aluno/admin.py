from django.contrib import admin

# Register your models here.
from aluno.models import *

admin.site.register(Aluno)
admin.site.register(Elo)
admin.site.register(SugestaoCurso)
