from django.db.models import QuerySet
from django.db.models.query import RawQuerySet
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from rest_framework.response import Response

from Utils.Except import generic_except
from avatar.models import AvatarHasAluno, Avatar
from avatar.serializers import AvatarHasAlunoSerializer, AvatarSerializer


class AvatarHasAlunoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = AvatarHasAluno.objects.all()
    serializer_class = AvatarHasAlunoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        data: dict = request.data
        try:
            avatar_select = AvatarHasAluno.objects.filter(aluno__user=request.user, is_active=True).first()
            if avatar_select is not None:
                avatar_select.is_active = False
                avatar_select.save()

            print(data['avatar_id']);
            if data['avatar_id'] is not None:
                avatar = AvatarHasAluno.objects.filter(aluno__user=request.user, avatar_id=data['avatar_id']).first()
                avatar.is_active = True
                avatar.save()
            return Response({'status': True})
        except Exception as ex:
            return generic_except(ex)

    def list(self, request, *args, **kwargs):
        data = self.serializer_class(self.queryset.filter(aluno__user=request.user), many=True).data
        return Response({'status': True, 'data': data})
