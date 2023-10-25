import os
import random
from urllib.parse import urljoin
from django.db import models
from django.utils import timezone
from django.conf import settings


def get_save_path(instance, filename=None):
    return os.path.join(settings.DATA_DIR, instance.path)


class File(models.Model):
    file = models.FileField(upload_to=get_save_path, storage=settings.FS)
    path = models.CharField()
    source = models.ForeignKey('Source', on_delete=models.CASCADE, related_name='files')
    group = models.ForeignKey('FileGroup', on_delete=models.CASCADE, related_name='files', blank=True, null=True)
    replicas = models.ManyToManyField('Node', related_name='files', blank=True)
    created_at = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'files'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(File, self).save(*args, **kwargs)

    @property
    def url(self):
        replicas = self.replicas.all()
        if not replicas:
            return None
        replica = random.choice(replicas)
        return urljoin(replica.static_url, self.path)
