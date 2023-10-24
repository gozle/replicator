import pika
import uuid
from replicator import rabbitmq


class NodeRpcClient:

    def __init__(self):
        self.channel = rabbitmq.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode('utf-8')

    def call(self, source):
        self.corr_id = uuid.uuid4().hex
        self.channel.basic_publish(
            exchange='',
            routing_key='nodes-round-robin',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=source
        )
        rabbitmq.process_data_events(time_limit=None)
        return self.response


# USAGE
# rpc = NodeRpcClient()
# source = 'gozle_video'
# for i in range(10000):
#     print(f" [x] Requesting node for source '{source}'")
#     response = rpc.call(source)
#     print(f" [.] Got {response}")
