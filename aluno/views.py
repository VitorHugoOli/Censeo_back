from django.db import IntegrityError
# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

from Utils.UsersExcept import verf_integrityerror, generic_except
from aluno.models import Aluno
from aluno.serializers import AlunoSerializer


class ProfessorViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

    # permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            aluno = Aluno(
                nome=data['name'],
                username=data['user'],
                email=data['email'],
                matricula=data['matricula'],
                lattes=data['lattes'],
            )
            aluno.set_password(data['pass'])
            aluno.save()

            return Response({'status': True, 'prof': AlunoSerializer(aluno)})
        except IntegrityError as ex:
            return verf_integrityerror(ex)
        except Exception as ex:
            return generic_except(ex)

    def list(self, request, *args, **kwargs):
        response = []

        for i in self.queryset:
            print(i.idprofessor)
            print(i.pk)
            print("\n")

        return Response({'status': "Opaaa"})
