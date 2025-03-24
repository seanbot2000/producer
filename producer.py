import pika
import faker
from datetime import datetime
import logging
from datetime import datetime, timezone
import time
import os

logging.basicConfig(level=logging.INFO, filename='demo.log')
username = 'user'
password = os.getenv('rabbitmq-password')


class Producer:

    def __init__(self):
        self._init_kafka_producer()

    def _init_kafka_producer(self):
        credentials = pika.PlainCredentials(username, password)
        parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='users')

    def publish_to_rabbit(self, message):
        try:
            self.channel.basic_publish(exchange='', routing_key='users', body=str(message))
        except Exception as e:
            logging.error(f"Exception {e}")
        else:
            logging.info(f"Published message {message} into queue.")

    @staticmethod
    def create_random_user():
        f = faker.Faker()

        new_user = dict(
            username=f.user_name(),
            first_name=f.first_name(),
            last_name=f.last_name(),
            email=f.email(),
            date_created=str(datetime.now(timezone.utc)),
        )

        return new_user


if __name__ == "__main__":
    producer = Producer()
    while True:
        random_user = producer.create_random_user()
        producer.publish_to_rabbit(random_user)

        time.sleep(5)
