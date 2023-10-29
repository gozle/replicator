import requests
from time import sleep
from django.conf import settings
from api.models import Node
from api.models.file import get_save_path


def worker():
    while 1:
        try:
            replicate()
            sleep(3)
        except Exception as e:
            print(e)
            sleep(1)


def replicate():
    try:
        this_node = Node.objects.get(id=settings.NODE_ID)
    except Node.DoesNotExist:
        print(f'{settings.NODE_ID} does not exist')
        return
    files = this_node.get_files_to_replicate()
    for file in files:
        status = save_file(file)
        if status:
            file.replicas.add(this_node)


def save_file(file):
    url = file.url
    if not url:
        print('no replicas', file.id, file.path)
        return None
    try:
        response = requests.get(file.private_url, stream=True)
    except Exception as e:
        print('[ERROR] static server not responds', url, e)
        return None
    path = get_save_path(file)
    with open(path, mode="wb") as f:
        for chunk in response.iter_content(chunk_size=10 * 1024):
            f.write(chunk)
    return True


if __name__ == '__main__':
    worker()
