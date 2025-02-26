from django.apps import AppConfig


class SaleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sale'

    def ready(self):
        import sale.signals  # Ensure signals are imported
