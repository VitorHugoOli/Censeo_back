from django.contrib import admin

# Register your models here.
from avaliacao.models import *


class AvaliacaoAdmin(admin.ModelAdmin):
    model = Avaliacao
    list_display = ('get_name', 'end_time', 'completa', 'aula', 'aluno')

    @staticmethod
    def get_name(obj: Avaliacao):
        return obj.aula.turma.codigo

    @staticmethod
    def aluno(obj: Avaliacao):
        return obj.aluno.user.nome


admin.site.register(Avaliacao, AvaliacaoAdmin)
admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(Caracteristica)
