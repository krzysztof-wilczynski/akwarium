from django.apps import AppConfig

from tasks import startup


class AquariumConfig(AppConfig):
    name = 'aquarium'

    def ready(self):
        startup()