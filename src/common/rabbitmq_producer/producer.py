import pika
from io import BytesIO
import numpy as np

class RabbitMQProducer:

    def __init__(self):

        self.load_configuration()

        print(f"Producer connecting to {self.params['host']}")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.params["host"])
        )


        self.channel = connection.channel()

        # Idempotent command. Just to ensure queue existence
        self.channel.queue_declare(queue=self.params["queue_name"])

    def load_configuration(self):
        # TODO: Read from env variables
        self.params={
            "host": "localhost",
            "queue_name": "test",
        }

    def send_img(self, img):
        np_bytes = BytesIO()
        np.save(np_bytes, img, allow_pickle=True)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.params["queue_name"],
            body=np_bytes.getvalue()
        )