#!/usr/bin/env python3

import pika
import time

conn_str = 'localhost'
message = 'test rabbit message'
qname = 'testq'
produce = 10000

conn = pika.BlockingConnection(pika.ConnectionParameters(conn_str))
channel = conn.channel()
channel.queue_declare(queue=qname)

for i in range(produce):
    channel.basic_publish(exchange='',
                      routing_key=qname,
                      body='message %d' % i)
    print('Produced message %d' % i)
    time.sleep(0.01)

conn.close()
