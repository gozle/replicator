from django.db import models


class Replication(models.Model):
    node = models.ForeignKey('Node', on_delete=models.CASCADE, related_name='replications')
    replicate = models.BooleanField(default=True)
    source = models.ForeignKey('Source', on_delete=models.CASCADE, related_name='replications')

    class Meta:
        db_table = 'replications'
        unique_together = [["node", "source"]]
