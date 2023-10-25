from urllib.parse import urljoin
import requests
from django.db import models


class Node(models.Model):
    id = models.CharField(primary_key=True)
    local_ip = models.GenericIPAddressField(unique=True)
    api_port = models.PositiveIntegerField(default=14000)
    static_url = models.URLField()

    @property
    def api_url(self):
        return f'http://{self.local_ip}:{self.api_port}/api'

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
