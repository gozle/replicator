import os.path
import pathlib
import threading
from time import sleep
from django.conf import settings
from api.models import File, Node


def fs_scanner():
    while 1:
        if threading.current_thread().stopped():
            return
        try:
            scan_data_dir()
            sleep(3)
        except Exception as e:
            print(e)
            sleep(1)


def scan_data_dir():
    try:
        this_node = Node.objects.get(id=settings.NODE_ID)
    except Node.DoesNotExist:
        print(f'{settings.NODE_ID} does not exist')
        return

    data_dir = settings.DATA_DIR
    paths = []
    for path, subdirs, files in os.walk(data_dir):
        for name in files:
            paths.append(pathlib.Path(path, name))

        if threading.current_thread().stopped():
            return
    for path in paths:
        relpath = os.path.relpath(path, data_dir)
        p = relpath.replace('\\', '/')

        try:
            file_in_db = File.objects.get(path=p)
        except File.DoesNotExist:
            file_in_db = None
        try:
            file_in_node = this_node.files.get(path=p)
        except File.DoesNotExist:
            file_in_node = None

        if not file_in_db:
            os.remove(path)
        elif file_in_db and not file_in_node:
            file_in_db.replicas.add(this_node)
