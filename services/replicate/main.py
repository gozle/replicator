import requests
from time import sleep
from django.conf import settings
from api.models import Replication, File, Node
from api.models.file import get_save_path


def worker():
    while 1:
        try:
            replicate()
        except Exception as e:
            print(e)
            sleep(1)


def replicate():
    try:
        this_node = Node.objects.get(id=settings.NODE_ID)
    except Node.DoesNotExist:
        print(f'{settings.NODE_ID} does not exist')
        return
    replications = Replication.objects.filter(replicate=True, node=this_node)
    files = File.objects.filter(source__in=[repl.source for repl in replications]).exclude(replicas__in=[this_node])
    for file in files:
        print(file.path)


def save_file(file):
    response = requests.get(file.url, stream=True)
    path = get_save_path(file)
    with open(path, mode="wb") as f:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            f.write(chunk)
