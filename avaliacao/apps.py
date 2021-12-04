from django.apps import AppConfig


class AvaliacaoConfig(AppConfig):
    name = 'avaliacao'

    def ready(self):
        from avaliacao import updater
        updater.start_strike()
        updater.start_rewards()
