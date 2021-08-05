from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.db.models import Count

from turma.models import Turma, AlunoHasTurma
from user.models import User


def formatbody(nome, senha, turmas):
    many_turmas = f"pois suas turmas da disciplinas {turmas}"
    single_turma = f"pois sua turma da disciplina {turmas}"
    turma_text: str
    if len(turmas):
        turma_text = many_turmas
    else:
        turma_text = single_turma
    return f"""
    Ol\u00E1 {nome}, espero que este email lhe encontre bem! \r\n\r\n
    Estou enviando este email, {', '.join(turmas)}, est\u00E1 participando da apura\u00E7\u00E3o de dados para meu Projeto de final de curso, e se poss\u00EDvel gostaria de contar com sua ajuda. \r\n\r\n
    Caso deseje participar, e n\u00E3o s\u00F3 me ajudar, mas como tamb\u00E9m o corpo docente participativo, ser\u00E1 muito f\u00E1cil, seus dados(Matr\u00EDcula, Nome e Email) 
    j\u00E1 est\u00E3o cadastrados no sistema do aplicativo agora basta entrar com a senha tempor\u00E1ria e avaliar as aulas ao final de cada uma delas ;)\r\n\r\n
    SENHA TEMPOR\u00C1RIA: {senha}
    \r\n\r\nAplicativo Android: XXXX
    \r\nAplicativo IOS: XXXX
    \r\n\r\nEstarei dispon\u00EDvel para responder quaisquer eventuais d\u00FAvidas, tanto nesse e mail, quanto em meu numero (31) 985168687.
    \r\n\r\nExplicando um pouco sobre meu projeto, ele visa aplicar conceitos sobre rede de sensores remotos(p. ex. redes de usu\u00E1rios com celulares) para captura e avalia\u00E7\u00E3o em tempo real de ambientes. 
    \r\n\r\nDessa forma, para desenvolver mais sobre este conceito criei um aplicativo para avalia\u00E7\u00E3o cont\u00EDnua da qualidade de aulas, no qual o aluno que participar desse projeto responde 10 perguntas ao final de cada aula de forma an\u00F4nima. 
    Ao final de cada aula e de forma acumulada durante o semestre os resultados dos question\u00E1rios preenchidos ser\u00E3o usados para guiar o professor sobre conceitos do qual este pode estar melhorando para as pr\u00F3ximas aulas e at\u00E9 para futuros semestres. O aplicativo ainda contar\u00E1 com um sistema de bonifica\u00E7\u00E3o para alunos mais participativos, este ser\u00E1 detalhado dentro do app.
    \r\n\r\nAtenciosamente,
    \r\nVitor Hugo Oliveira Silva\r\n\r\n\r\n\r\n\r\n
    """


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            users = User.objects.filter(tipo_user='Aluno')
            for i in users:
                turmas = AlunoHasTurma.objects.filter(aluno__user=i).values_list('turma__codigo', flat=True)
                password = User.objects.make_random_password(length=8)
                i.set_password(password)
                i.save()
                send_mail(
                    'Senha aplicativo censeo',
                    formatbody(i.nome, password, turmas),
                    'vitor.h.oliveira@ufv.br',
                    [i.email],
                    fail_silently=False
                )
            print("EMAIL ENVIADO COM SUCESSO")
        except Exception as ex:
            print(ex)
            print("Houve algum erro ao disparar os emails!")
