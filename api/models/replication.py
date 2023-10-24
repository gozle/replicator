from django.db import models


class Replication(models.Model):
    node = models.OneToOneField('Node', on_delete=models.CASCADE, related_name='replications')
    replicate = models.BooleanField(default=True)
    sources = models.ManyToManyField('Source', blank=True, related_name='replications')

    class Meta:
        db_table = 'replications'
