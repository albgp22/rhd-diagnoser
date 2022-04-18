import pika
from io import BytesIO
import numpy as np
import matplotlib.pyplot as plt

class RabbitMQConsumer:

    def __init__(self):

        self.loadConfiguration()
        print(f"Consumer connecting to {self.params['host']}")

        connection = pika.BlockingConnection(
            pika.ConnectionParameters(self.params["host"])
        )

        self.channel = connection.channel()

        # Idempotent command. Just to ensure queue existence
        self.channel.queue_declare(queue=self.params["queue_name"])

    def loadConfiguration(self):
        self.params={
            "host": "localhost",
            "queue_name": "test",
        }

    def img_callback(ch, method, properties, body):
        print("Reading from queue")
        load_bytes = BytesIO(body)
        loaded_np = np.load(load_bytes, allow_pickle=True)
        plt.imshow(loaded_np)
        plt.show()


    def consume_img(self, callback):
        self.channel.basic_consume(
            queue=self.params["queue_name"],
            auto_ack=True,
            on_message_callback=callback
        )
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()