import os
from django.db import models
from django.utils import timezone
from django.conf import settings


def get_save_path(instance, filename):
    return os.path.join(settings.DATA_DIR, instance.path)


class File(models.Model):
    file = models.FileField(upload_to=get_save_path, storage=settings.FS)
    path = models.CharField()
    source = models.ForeignKey('Source', on_delete=models.CASCADE, related_name='files')
    group = models.ForeignKey('FileGroup', on_delete=models.CASCADE, related_name='files', blank=True, null=True)
    replications = models.ManyToManyField('Replication', blank=True, related_name='files')
    created_at = models.DateTimeField(blank=True)

    class Meta:
        db_table = 'files'

    def save(self, *args, **kwargs):
        if not self.id:
            self.created_at = timezone.now()
        return super(File, self).save(*args, **kwargs)
