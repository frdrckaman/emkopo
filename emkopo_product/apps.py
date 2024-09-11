from django.apps import AppConfig as DjangoAppConfig


class AppConfig(DjangoAppConfig):
    name = 'emkopo_product'

    def ready(self):
        import emkopo_product.models.signals


