from django.contrib import admin

# Register your models here.
from avaliacao.models import *

admin.site.register(Avaliacao)
admin.site.register(Pergunta)
admin.site.register(Resposta)
admin.site.register(Caracteristica)
