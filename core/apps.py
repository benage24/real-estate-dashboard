from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals

# class RentalConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'rental'
#     def ready(self):
#         import core.signals

