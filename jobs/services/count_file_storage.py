from django.db.models import F
from ..models import UploadStats


def count_file_storage(size_bytes: int):
    UploadStats.objects.get_or_create(id=1)

    UploadStats.objects.filter(id=1).update(
        total_files_processed=F("total_files_processed") + 1,
        total_storage_processed=F("total_storage_processed") + size_bytes,
    )
