# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response

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
            prof.set_password(data['pass'])
            prof.save()

            return Response({'status': True})
        except Exception as e:
            return Response({'status': False, 'error': e.__str__()})

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
