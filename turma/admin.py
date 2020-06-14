from django.contrib import admin

# Register your models here.
from turma.models import *

admin.site.register(Turma)
admin.site.register(DiasFixos)
admin.site.register(TopicaTurma)
admin.site.register(SugestaoTurma)
admin.site.register(ProfessorHasTurma)
admin.site.register(AlunoHasTurma)
