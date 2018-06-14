#!/usr/bin/env python
import uuid, pika


class QueueConsumer(object):

    def __init__(self):
        credentials = pika.PlainCredentials('guest', 'guest')
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost', 5672, '/', credentials))
        channel = connection.channel()
        exchange = 'exchange-a'
        queue = str(uuid.uuid4())
        channel.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
        channel.queue_declare(queue=queue, durable=True) 
        channel.queue_bind(exchange=exchange, queue=queue)
        channel.basic_qos(prefetch_count=1)  # In order to spread the load equally over multiple servers
        channel.basic_consume(self.on_request, queue=queue)
        print('Consumer WAITING ({0})'.format(queue))
        channel.start_consuming()

    def on_request(self, ch, method, props, body):
        n = str(body)
        print('Consumer IN: {0}'.format(n))
        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=str(n))
        ch.basic_ack(delivery_tag=method.delivery_tag)
        print('Consumer OUT: {0}'.format(n))
        print()
