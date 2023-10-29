from django.db import models


class FileGroup(models.Model):
    id = models.CharField(primary_key=True)

    class Meta:
        db_table = 'file_groups'
