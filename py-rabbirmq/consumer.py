#!/usr/bin/env python3

import pika
import time

conn_str = 'localhost'
qname = 'testq'

conn = pika.BlockingConnection(pika.ConnectionParameters(conn_str))
channel = conn.channel()
channel.queue_declare(queue=qname)

def callback(ch, method, properties, body):
    print("Consumed %s" % body)

channel.basic_consume(queue=qname,
                      auto_ack=True,
                      on_message_callback=callback)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
