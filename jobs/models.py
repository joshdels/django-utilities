from django.db import models


class UploadStats(models.Model):
    total_files_processed = models.BigIntegerField(default=0)
    total_storage_processed = models.BigIntegerField(default=0)
