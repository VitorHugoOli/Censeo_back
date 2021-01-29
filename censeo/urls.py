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

from aluno import views as views_aluno
from aula import views as views_aulas
from curso import views as views_curso
from faculdade_sugestao import views as views_facu
from professor import views as views_prof
from turma import views as views_turma
from user import views as views_user
from avaliacao import views as views_aval

router = routers.DefaultRouter()
router.register(r'user', views_user.UserViewSet)
router.register(r'login', views_user.LoginViewSet, basename='login')
router.register(r'prof', views_prof.ProfessorViewSet)
router.register(r'curso', views_curso.CursoViewSet)
router.register(r'aluno', views_aluno.AlunoViewSet)
router.register(r'aulas', views_aulas.AulaViewSet)
router.register(r'turmas', views_turma.TurmaViewSet)
router.register(r'schedule', views_turma.DiasFixosViewSet)
router.register(r'topicosTurma', views_turma.TopicaTurmaViewSet)
router.register(r'sugestaoTurma', views_turma.SugestaoTurmaViewSet)
router.register(r'topicosCurso', views_aluno.TopicoSugestaoCursoViewSet)
router.register(r'sugestaoCurso', views_aluno.SugestaoCursoViewSet)
router.register(r'topicosFacu', views_facu.TopicoFaculdadeViewSet)
router.register(r'sugestaoFacu', views_facu.SugestaoFaculdadeViewSet)
router.register(r'avaliacao', views_aval.AvaliacaoViewSet)
router.register(r'resposta', views_aval.RespostaViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('aluno/suggestionCategories', views_aluno.get_suggestions_categories),
    path('prof/suggestionCategories', views_prof.get_suggestions_categories),
    path('aulas_abertas/', views_aulas.get_professor_class_open),
    path('endClass/', views_aulas.put_class_end),
    path('alunoAulas/', views_aulas.get_aluno_class_open),
    path('aulasTurma/<int:id>', views_aulas.retrieve_aula_from_turma),
    path('turmas/<int:id>/alunos', views_turma.pupils_list),
    path('admin/', admin.site.urls),
    url(r'^api-auth/', include('rest_framework.urls'))
]
