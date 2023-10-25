from django.db import models


class FileGroup(models.Model):

    class Meta:
        db_table = 'file_groups'
