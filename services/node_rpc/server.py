import pika
import itertools
from django.utils import timezone
from replicator import rabbitmq
from api.models import Replication, Source


channel = rabbitmq.channel()

round_robin_queues = {}
last_updated = None
channel.queue_declare(queue='nodes-round-robin')


def update_nodes():
    global round_robin_queues
    for source in Source.objects.all():
        replications = Replication.objects.filter(source=source, replicate=True)
        round_robin_queues[source.id] = itertools.cycle([replication.node.id for replication in replications])


def on_request(ch, method, props, body):
    global last_updated
    source = body.decode()

    if not last_updated or (timezone.now() - last_updated) > timezone.timedelta(seconds=10):
        update_nodes()
        last_updated = timezone.now()

    print(f' [.] node for source "{source}"')
    queue = round_robin_queues.get(source)
    if queue:
        try:
            response = str(next(queue))
            print(f' [.] ({source}) found node {response}')
        except StopIteration:
            response = ''
            print(f' [.] ({source}) no nodes for this source ')
    else:
        response = ''
        print(f' [.] ({source}) does not exists')

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='nodes-round-robin', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
