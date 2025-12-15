from django.apps import AppConfig


class XpressvegConfig(AppConfig):
     DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

     name = 'xpressveg'

     def ready(self):
         import xpressveg.signals
