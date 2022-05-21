from django.apps import AppConfig
import time

class SheetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sheets'

    def ready(self) -> None:
        from .management.commands import runapscheduler
        # runapscheduler.scheduler.start()
