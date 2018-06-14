#!/usr/bin/env python
import pika, uuid


class QueueProducer(object):

    def __init__(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
        self.channel = self.connection.channel()
        self.reply_to = str(uuid.uuid4())
        self.exchange = 'exchange-a'
        self.channel.queue_declare(queue=self.reply_to, durable=True)
        self.channel.queue_bind(exchange=self.exchange, queue=self.reply_to)
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.reply_to)

    def on_response(self, ch, method, props, body):
        self.response = body.decode('utf-8')
        if self.correlation_id == props.correlation_id:
            print('producer response: {0}'.format(self.response))

    def processar(self, n):
        self.response = None
        self.correlation_id = str(uuid.uuid4())
        self.channel.basic_publish(exchange=self.exchange,
                                   routing_key='',
                                   properties=pika.BasicProperties(
                                         reply_to=self.reply_to,
                                         correlation_id=self.correlation_id),
                                   body=str(n))
        while self.response is None:
            self.connection.process_data_events()
        print('producer processar ended: {0}'.format(self.response))
