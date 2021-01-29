from django.apps import AppConfig


class AvaliacaoConfig(AppConfig):
    name = 'avaliacao'

    def ready(self):
        from avaliacao import updater
        updater.start_week()
        updater.start_rewards()
