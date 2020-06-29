# Create your views here.
import re

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response

from Utils.Except import verf_user_integrityerror, generic_except
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from professor.models import Professor
from professor.serializers import ProfessorSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            prof = Professor(
                nome=data['name'],
                username=data['user'],
                email=data['email'],
                matricula=data['matricula'],
                lattes=data['lattes'],
            )
            validate_password(data['pass'])
            prof.set_password(data['pass'])
            prof.save()

            return Response({'status': True, 'prof': ProfessorSerializer(prof).data})
        except IntegrityError as ex:
            return verf_user_integrityerror(ex)
        except ValidationError:
            message = "Sua senha é muito simples. Dicas: Ela tem que ter mais de 8 digitos e não pode conter só numeros"
            return Response({'status': False,
                             'error': message})
        except Exception as ex:
            return generic_except(ex)


class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        data = request.data
        login = data['login']
        password = data['pass']

        userTypes = [Professor, Aluno]

        def generic_verf(query):
            try:
                obj = query()
                if obj.check_password(password):
                    if type(obj) == Professor:
                        tipo = 'professor'
                        user = ProfessorSerializer(obj).data
                    else:
                        tipo = 'aluno'
                        user = AlunoSerializer(obj).data
                    return Response({'status': True, 'type': tipo, 'user': user})
                else:
                    return Response({'status': False, 'error': 'Senha incorreta.'})
            except ObjectDoesNotExist as ex:
                return None
            except Exception as ex:
                generic_verf(ex)

        def verf_email(entity):
            return generic_verf(lambda: entity.objects.get(email=login))

        def verf_user_name(entity):
            return generic_verf(lambda: entity.objects.get(username=login))

        def verf_matricula(entity):
            return generic_verf(lambda: entity.objects.get(matricula=login))

        if '@' in login:
            for i in userTypes:
                resp = verf_email(i)
                if resp:
                    return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhum email correspondente.'})
        elif re.search("\d+", login):
            for i in userTypes:
                resp = verf_matricula(i)
                if resp:
                    return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhuma matricula correspondente.'})
        else:
            for i in userTypes:
                resp = verf_user_name(i)
                if resp:
                    return resp
            return Response({'status': False, 'error': 'Não foi identificamos nenhum login correspondente.'})
