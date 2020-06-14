from django.contrib import admin

# Register your models here.
from avaliacao.models import *

admin.site.register(Avaliacoes)
admin.site.register(Perguntas)
admin.site.register(Respostas)
admin.site.register(Caracteristica)
