from django.apps import AppConfig


class UsageConfig(AppConfig):
    name = 'wingtel.usage'
    label = 'usage'

    def ready(self):
        import wingtel.usage.signals
