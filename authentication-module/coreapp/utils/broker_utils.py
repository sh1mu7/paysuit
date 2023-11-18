import json
import threading
import pika
from django.conf import settings

from coreapp.utils import consumers

SERVER_URL = "amqp://admin:password@openmedia.local/"
QUEUE_PATH = "paysuite"


def publish_event(event, data):
    parameters = pika.URLParameters(SERVER_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    properties = pika.BasicProperties(event)
    channel.basic_publish(exchange='', routing_key=QUEUE_PATH, body=json.dumps(data), properties=properties)


class AMQPConsuming(threading.Thread):

    def callback(self, ch, method, properties, body):
        data = json.loads(body)
        event = properties.content_type
        if event == "payment_completed":
            consumers.payment_completed(data)
        if event == "settlement_complete":
            consumers.settlement_complete(data)

    @staticmethod
    def _get_connection():
        parameters = pika.URLParameters(SERVER_URL)
        return pika.BlockingConnection(parameters)

    def run(self):
        connection = self._get_connection()
        channel = connection.channel()
        channel.basic_consume(queue=QUEUE_PATH, on_message_callback=self.callback, auto_ack=True)
        channel.start_consuming()
