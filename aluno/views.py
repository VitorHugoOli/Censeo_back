from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import IntegrityError
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from Utils.Except import verf_user_integrityerror, generic_except
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer
from curso.models import Curso


class AlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            try:
                curso = Curso.objects.get(idcurso=data.get('curso'))
            except ObjectDoesNotExist as ex:
                curso = None

            aluno = Aluno(
                nome=data['name'],
                username=data['user'],
                email=data['email'],
                matricula=data['matricula'],
                curso_idcurso=curso
            )
            validate_password(data['pass'])
            aluno.set_password(data['pass'])
            aluno.save()

            return Response({'status': True, 'aluno': AlunoSerializer(aluno).data})
        except IntegrityError as ex:
            return verf_user_integrityerror(ex)
        except ValidationError:
            return Response({'status': False,
                             'error': "Sua senha é muito simples. Dicas: Ela tem que ter mais de 8 digitos e não pode conter só numeros"})
        except Exception as ex:
            return generic_except(ex)


