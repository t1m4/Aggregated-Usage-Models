from django.apps import AppConfig


class UsageConfig(AppConfig):
    name = 'wingtel.usage'
    label = 'usage'

    def ready(self):
        from wingtel.usage.signals import ready
        ready()
