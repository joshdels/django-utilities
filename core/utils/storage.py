from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os


def upload_file_to_b2(local_path: str, remote_path: str) -> str:
    """
    Upload local file to Backblaze (via Django storage)
    Returns public URL
    """

    with open(local_path, "rb") as f:
        file_data = f.read()

    saved_path = default_storage.save(remote_path, ContentFile(file_data))

    return default_storage.url(saved_path)
