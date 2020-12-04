from django.contrib import admin

# Register your models here.
from faculdade_sugestao.models import TopicoFaculdade, SugestaoFaculdade

admin.site.register(TopicoFaculdade)
admin.site.register(SugestaoFaculdade)
