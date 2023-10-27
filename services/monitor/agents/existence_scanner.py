import os.path
import threading
from time import sleep
from django.conf import settings
from api.models import Node
from api.models.file import get_save_path


def existence_scanner():
    while 1:
        if threading.current_thread().stopped():
            return
        try:
            scan_files()
            sleep(3)
        except Exception as e:
            print(e)
            sleep(1)


def scan_files():
    try:
        this_node = Node.objects.get(id=settings.NODE_ID)
    except Node.DoesNotExist:
        print(f'{settings.NODE_ID} does not exist')
        return
    files = this_node.files.all()
    for file in files:
        if threading.current_thread().stopped():
            return
        # print('[FILE]', file.id)
        exist = check_existence(file)
        if not exist:
            file.replicas.remove(this_node)


def check_existence(file):
    path = get_save_path(file)
    return os.path.exists(path)
