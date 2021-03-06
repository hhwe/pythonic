import sys
import pika


message = "".join(sys.argv[1:]) or "Hello World!"


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')


# 向hello队列仍任务
channel.basic_publish(
    exchange='',
    routing_key='hello',
    body=message
)


print("[X] Send %r" % message)


connection.close()
