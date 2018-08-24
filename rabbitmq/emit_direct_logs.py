import sys
import pika


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')


severity = sys.argv[1] if len(sys.argv) >= 2 else 'info'
print(sys.argv)
message = " ".join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(
    exchange='direct_logs',
    routing_key=severity,
    body=message,
)


print("[X] Send %r:%r" % (severity, message))
connection.close()
