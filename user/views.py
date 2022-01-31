import re

from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.db import IntegrityError
# Create your views here.
from firebase_admin import messaging
from rest_framework import viewsets
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
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

    def create(self, request: Request, *args, **kwargs):
        try:
            data: dict = request.data

            user = User(
                nome=data.get('name'),
                username=User.normalize_username(data['user']) if 'user' in data else None,
                matricula=data.get('matricula'),
                email=User.normalize_email(data['email']) if 'email' in data else None,
                tipo_user=data['tipo_user'] if 'tipo_user' in data else 'Aluno',
            )
            validate_password(data['pass'])
            user.set_password(data['pass'])
            user.save()

            context = UserSerializer(user).data
            if 'tipo_user' not in data:
                raise Exception('Tipo User deve ser passado')
            if data['tipo_user'] == 1:
                prof = Professor(
                    lattes=data.get('lattes'),
                    user=user,
                )
                prof.save()
                context['prof_id'] = prof.pk
            else:
                try:
                    curso = Curso.objects.get(id=data.get('curso'))
                except ObjectDoesNotExist as ex:
                    curso = None
                aluno = Aluno(
                    xp=0,
                    curso_idcurso=curso,
                    user=user
                )
                aluno.save()
                context['prof_id'] = aluno.pk

            return Response({'status': True, 'user': context})
        except IntegrityError as ex:
            return verf_user_integrityerror(ex)
        except ValidationError:
            return Response({'status': False,
                             'error': "Sua senha é muito simples. Dicas: Ela tem que ter mais de 8 digitos e não pode conter só numeros"})
        except Exception as ex:
            return generic_except(ex)

    def update(self, request, *args, **kwargs):
        try:
            data: dict = request.data
            id_user = kwargs['pk']

            if int(id_user) != int(request.user.id):
                raise Exception("Voce deve estar logado como esse usuário para alterá-lo")

            if request.user == AnonymousUser and request.auth is not None:
                raise Exception("Voce deve estar logado no sistema")

            if 'pass' in data:
                user = User.objects.get(id=id_user)
                validate_password(data['pass'])
                user.set_password(data['pass'])
                user.save()
            else:
                user = User.objects.filter(id=id_user)
                user.update(
                    nome=data['nome'],
                    username=User.normalize_username(data['username']) if 'username' in data else None,
                    email=User.normalize_email(data['email']),
                )
                user = user[0]

            if 'first_time' in data:
                user.first_time = False
                user.save()

            context = UserSerializer(user).data

        except IntegrityError as ex:
            return verf_user_integrityerror(ex)
        except ValidationError:
            return Response({'status': False,
                             'error': "Sua senha é muito simples.\nDicas: Ela tem que ter mais de 8 digitos e não pode conter só numeros"})
        except Exception as ex:
            return generic_except(ex)
        return Response({'status': True, 'user': context})


class LoginViewSet(viewsets.ViewSet):
    def create(self, request):
        data = request.data
        try:
            login = data['login']
            password = data['pass']

            def generic_verify(query):
                try:
                    obj = query()
                    if obj.check_password(password):
                        context = UserSerializer(obj).data
                        if obj.tipo_user == "Professor":
                            context['typeId'] = ProfessorSerializer(Professor.objects.get(user=obj)).data.get("id")
                        else:
                            context['typeId'] = AlunoSerializer(Aluno.objects.get(user=obj)).data.get("id")
                            context['perfilPhoto'] = AlunoSerializer(Aluno.objects.get(user=obj)).data.get(
                                "perfilPhoto")
                        return Response({'status': True, 'user': context})
                    else:
                        return Response({'status': False, 'error': 'Senha incorreta.'})
                except ObjectDoesNotExist as ex:
                    return Response({'status': False, 'error': 'Usuário não existe.'})
                except Exception as ex:
                    return generic_except(ex)

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
                return Response({'status': False, 'error': 'Nenhum email correspondente.'})
            elif re.search(r'\d+', login):
                resp = verify_matricula()
                if resp:
                    return resp
                return Response({'status': False, 'error': 'Nenhuma matricula correspondente.'})
            else:
                resp = verify_user_name()
                if resp:
                    return resp
                return Response({'status': False, 'error': 'Nenhum username correspondente.'})
        except Exception as ex:
            return generic_except(ex)


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def push_token(request):
    try:
        user = request.user
        if request.method == 'POST':
            data = request.data
            if 'token' in data:
                token = data['token']
                user.push_token = token
                user.save()
                return Response({'status': True})
            else:
                return Response({'status': False, 'error': 'Token não informado'})
        else:
            if user.push_token:
                return Response({'status': True, 'token': user.push_token})
            else:
                return Response({'status': False, 'error': 'Token não informado'})
    except Exception as ex:
        return generic_except(ex)


def send_push(title, body, registration_tokens,*args, **kwargs):
    try:
        message = messaging.MulticastMessage(
            notification=messaging.Notification(title=title, body=body),
            tokens=registration_tokens)
        response = messaging.send_multicast(message)
        print('Successfully sent message:', response)
    except Exception as ex:
        print('Error sending message:', ex)
