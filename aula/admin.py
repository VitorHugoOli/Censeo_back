from django.contrib import admin

# Register your models here.
from aula.models import *


def aula(obj):
    return obj.turma.codigo + " " + obj.dia_horario.__str__()


class aulaAdmin(admin.ModelAdmin):
    model = Aula
    list_display = (aula, 'is_aberta_avaliacao', 'is_aberta_class')


admin.site.register(Aula, aulaAdmin)
admin.site.register(Prova)
admin.site.register(Teorica)
admin.site.register(TrabalhoPratico)
admin.site.register(Excursao)
