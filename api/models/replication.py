from django.db import models


class Replication(models.Model):
    source = models.OneToOneField('Source', on_delete=models.CASCADE, related_name='replications')
    nodes = models.ManyToManyField('Node', blank=True, related_name='replications')
    replicate = models.BooleanField(default=True)

    class Meta:
        db_table = 'replications'
