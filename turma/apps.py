from django.apps import AppConfig


class TurmaConfig(AppConfig):
    name = 'turma'

    def ready(self):
        from turma import updater
        updater.start()
