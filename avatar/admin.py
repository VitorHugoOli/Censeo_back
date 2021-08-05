from django.contrib import admin

# Register your models here.
from avatar.models import *

admin.site.register(Avatar)
admin.site.register(AvatarHasAluno)
