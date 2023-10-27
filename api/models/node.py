import requests
from urllib.parse import urljoin
from django.db import models
from api.models.replication import Replication
from api.models.file import File


class Node(models.Model):
    id = models.CharField(primary_key=True)
    local_ip = models.GenericIPAddressField(unique=True)
    api_port = models.PositiveIntegerField(default=14000)
    static_url = models.URLField()

    @property
    def api_url(self):
        return f'http://{self.local_ip}:{self.api_port}/api'

    def get_files_to_replicate(self):
        replications = Replication.objects.filter(replicate=True, node=self)
        files = (File.objects.filter(source__in=[repl.source for repl in replications])
                 .exclude(replicas__in=[self]))
        return files

    def file_exists(self, pk):
        try:
            resp = requests.get(urljoin(self.api_url, f'files/{pk}/exists'))
            status = resp.json()
            return status
        except Exception as e:
            print(e)
            return None

    class Meta:
        db_table = 'nodes'
