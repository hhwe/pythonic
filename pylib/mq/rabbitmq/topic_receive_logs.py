import time
import sys
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(exclusive=True)
queue_name = result.method.queue


severities = sys.argv[1:]
print(severities)
if not severities:
    sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(-1)


# * (star) can substitute for exactly one word.
# # (hash) can substitute for zero or more words.
for severity in severities:
    channel.queue_bind(
        exchange='topic_logs',
        queue=queue_name,
        routing_key=severity,
    )
print(" [*] Waiting for messages. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print("[x] Received %r:%r" % (method.routing_key, body))


channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)


channel.start_consuming()
