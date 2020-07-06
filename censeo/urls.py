"""censeo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from curso import views as views_curso
from user import views as views_user
from professor import views as views_prof
from aluno import views as views_aluno

router = routers.DefaultRouter()
router.register(r'user', views_user.UserViewSet)
router.register(r'login', views_user.LoginViewSet, basename='login')
router.register(r'prof', views_prof.ProfessorViewSet)
router.register(r'curso', views_curso.CursoViewSet)
router.register(r'aluno', views_aluno.AlunoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'))
]
