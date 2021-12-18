from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail, send_mass_mail
from django.core.management import BaseCommand
from django.db.models import Count

from turma.models import Turma, AlunoHasTurma
from user.models import User


def formatbody(nome, senha, turmas):
    many_turmas = f"pois suas turmas das disciplinas {' ,'.join(turmas)}"
    single_turma = f"pois sua turma da disciplina {''.join(turmas)}"
    turma_text: str

    if len(turmas) > 1:
        turma_text = many_turmas
    else:
        turma_text = single_turma

    return f"Olá {nome}, espero que este email lhe encontre bem! \n\nEstou enviando este email, {turma_text}, está participando da coleta de dados para meu Projeto de final de " \
           f"curso, e, se possível, gostaria de contar com sua ajuda. \n\nExplicando um pouco sobre meu projeto, ele visa aplicar conceitos sobre rede de sensoriamento " \
           f"participativo (p. ex. redes de usuários com celulares) para captura e avaliação em tempo real de ambientes. \n\nDessa forma, para desenvolver mais sobre este " \
           f"conceito, criei um aplicativo para avaliação contínua da qualidade de aulas, no qual o aluno que participar desse projeto responde 10 perguntas ao final de cada " \
           f"aula de forma anônima. Ao final de cada aula e de forma acumulada durante o semestre os resultados dos questionários preenchidos serão usados para guiar o professor " \
           f"sobre conceitos que podem ser melhorados para as próximas aulas e até para futuros semestres. O aplicativo ainda contará com um sistema de gamificação e bonificação " \
           f"para alunos mais participativos. \n\nA gamificação se dará de duas formas: a primeira por meio de um ranking da turma avaliando alunos mais participativos. Esse " \
           f"ranking ao final do semestre talvez poderá ser usado para uma possível distribuição de pontos extras na disciplina. A segunda forma será através das avaliações " \
           f"semanais, em que o aluno que avaliar todas as aulas em um tempo menor que 20 minutos, receberá um avatar shine e os alunos que responderem todas as avaliações em " \
           f"menos de 60 minutos  receberão um novo avatar.   \n\nCaso deseje participar, será muito fácil: seus dados (Matrícula, Nome e E-mail) já estão cadastrados no sistema " \
           f"do aplicativo. Agora basta entrar com a senha temporária e avaliar as aulas ao final de cada uma delas ;)\n\nSENHA TEMPORÁRIA: {senha}\n\nAplicativo Android: " \
           f"https://play.google.com/store/apps/details?id=com.poc.censeo\nAplicativo IOS: https://apps.apple.com/br/app/censeo/id1579915960?l=en\n\nEstarei disponível para " \
           f"responder quaisquer eventuais dúvidas, tanto nesse e-mail, quanto em meu número (31) 985168687.\n\nAtenciosamente,\nVitor Hugo Oliveira Silva "


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            users = User.objects.filter(tipo_user='Aluno')
            user_emails = []
            for i in users:
                turmas = AlunoHasTurma.objects.filter(aluno__user=i).values_list('turma__codigo', flat=True)
                password = User.objects.make_random_password(length=8)
                i.set_password(password)
                i.save()
                user_emails.append((
                    'Senha aplicativo censeo',
                    formatbody(i.nome, password, turmas),
                    'vitor.h.oliveira@ufv.br',
                    [i.email],
                ))
            send_mass_mail(user_emails)
            print("EMAIL ENVIADO COM SUCESSO")
        except Exception as ex:
            print(ex)
            print("Houve algum erro ao disparar os emails!")
