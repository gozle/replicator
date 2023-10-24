from django.db import models


class Source(models.Model):
    id = models.CharField(primary_key=True)
    max_replicas = models.IntegerField(null=True, blank=True)
    directory = models.CharField()

    class Meta:
        db_table = 'sources'
