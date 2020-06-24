from django.db import IntegrityError
from rest_framework.response import Response


def verf_integrityerror(ex: IntegrityError):
    if 'email_UNIQUE' in ex.args[1]:
        return Response({'status': False, 'error': "Email repetido, entre com outro."})
    elif 'matricula_UNIQUE' in ex.args[1]:
        return Response({'status': False, 'error': "Matricula repetido, entre com outro."})
    elif 'username_UNIQUE' in ex.args[1]:
        return Response({'status': False, 'error': "Username repetido, entre com outro."})
    else:
        return Response({'status': False, 'error': "Algo de errado não está certo", 'except': ex.args})


def generic_except(ex: Exception):
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(ex).__name__, ex.args)
    print(message)
    return Response({'status': False, 'error': "Algo de errado não está certo", 'except': message})
