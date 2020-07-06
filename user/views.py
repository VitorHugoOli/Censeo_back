import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from Utils.Except import verf_user_integrityerror, generic_except
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from curso.models import Curso
from professor.models import Professor
from professor.serializers import ProfessorSerializer
from user.models import User
from user.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data

            user = User(
                nome=data['name'],
                username=User.normalize_username(data['user']),
                matricula=data['matricula'],
                email=User.normalize_email(data['email']),
                tipo_user=data['tipo_user'],
            )
            validate_password(data['pass'])
            user.set_password(data['pass'])
            user.save()

            context = UserSerializer(user).data
            if data['tipo_user'] == 1:
                prof = Professor(
                    lattes=data.get('lattes'),
                    user_iduser=user,
                )
                prof.save()
                context['prof_id'] = prof.pk
            else:
                try:
                    curso = Curso.objects.get(idcurso=data.get('curso'))
                except ObjectDoesNotExist as ex:
                    curso = None
                aluno = Aluno(
                    xp=0,
                    curso_idcurso=curso,
                    user_iduser=user
                )
                aluno.save()
                context['prof_id'] = aluno.pk

            # context['token'] = Token.objects.get(user=user).key
            return Response({'status': True, 'user': context})
        except IntegrityError as ex:
            return verf_user_integrityerror(ex)
        except ValidationError:
            return Response({'status': False,
                             'error': "Sua senha é muito simples. Dicas: Ela tem que ter mais de 8 digitos e não pode conter só numeros"})
        except Exception as ex:
            return generic_except(ex)


class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        login = data['login']
        password = data['pass']

        def generic_verify(query):
            try:
                obj = query()
                if obj.check_password(password):
                    context = UserSerializer(obj).data
                    if obj.tipo_user == "Professor":
                        context['professor'] = ProfessorSerializer(Professor.objects.get(user_iduser=obj)).data
                    else:
                        context['aluno'] = AlunoSerializer(Aluno.objects.get(user_iduser=obj)).data
                    return Response({'status': True, 'user': context})
                else:
                    return Response({'status': False, 'error': 'Senha incorreta.'})
            except ObjectDoesNotExist as ex:
                return None
            except Exception as ex:
                generic_verify(ex)

        def verify_email():
            return generic_verify(lambda: User.objects.get(email=login))

        def verify_user_name():
            return generic_verify(lambda: User.objects.get(username=login))

        def verify_matricula():
            return generic_verify(lambda: User.objects.get(matricula=login))

        if '@' in login:
            resp = verify_email()
            if resp:
                return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhum email correspondente.'})
        elif re.search(r'\d+', login):
            resp = verify_matricula()
            if resp:
                return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhuma matricula correspondente.'})
        else:
            resp = verify_user_name()
            if resp:
                return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhum login correspondente.'})
