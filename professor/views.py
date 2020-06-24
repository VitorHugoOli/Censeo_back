# Create your views here.
from django.contrib.auth.password_validation import MinimumLengthValidator, validate_password
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response

from Utils.UsersExcept import verf_integrityerror, generic_except
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
            return verf_integrityerror(ex)
        except ValidationError as ex:
            return Response({'status': False, 'error': ex.args})
        except Exception as ex:
            return generic_except(ex)

    def list(self, request, *args, **kwargs):
        response = []

        for i in self.queryset:
            print(i.idprofessor)
            print(i.pk)
            print("\n")

        return Response({'status': "Opaaa"})


class LoginViewSet(viewsets.ViewSet):

    def create(self, request):
        return Response({'status': "Opaaa"})
