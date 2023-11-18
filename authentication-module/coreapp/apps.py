from django.apps import AppConfig
from .utils import broker_utils
from .utils.broker_utils import AMQPConsuming


class CoreappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'coreapp'

    def ready(self):
        consumer = AMQPConsuming()
        consumer.daemon = True
        consumer.start()
