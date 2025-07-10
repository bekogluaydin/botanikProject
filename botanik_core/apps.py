from django.apps import AppConfig


class BotanikCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'botanik_core'

    # Bu işlem ile signals.py dosyamızı apps.py'a bağladık.
    def ready(self):
        import botanik_core.signals