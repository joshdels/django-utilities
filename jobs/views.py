import os
import uuid
from core.celery import app
from core.utils.converter import bytes_to_mb, bytes_to_gb
from celery.result import AsyncResult
from django.http import JsonResponse, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from .models import UploadStats
from .tasks import process_dxf_task


@api_view(["POST"])
@permission_classes([AllowAny])
def process_dxf(request):

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return HttpResponse("No file uploaded", status=400)

    original_name = uploaded_file.name

    MEDIA_DIR = "/app/media/tmp"
    os.makedirs(MEDIA_DIR, exist_ok=True)

    file_id = str(uuid.uuid4())
    temp_path = os.path.join(MEDIA_DIR, f"{file_id}.dxf")

    with open(temp_path, "wb") as f:
        for chunk in uploaded_file.chunks():
            f.write(chunk)

    task = process_dxf_task.delay(temp_path, original_name)

    return JsonResponse(
        {"message": "Processing started", "task_id": task.id}, status=202
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def task_status(request, task_id):

    result = AsyncResult(task_id, app=app)

    if result.state == "PENDING":
        return JsonResponse({"status": "pending"})

    elif result.state == "PROGRESS":
        return JsonResponse({"status": "processing", "step": result.info.get("step")})

    elif result.state == "SUCCESS":
        return JsonResponse(
            {"status": "done", "file_url": result.result.get("file_url")}
        )

    elif result.state == "FAILURE":
        return JsonResponse({"status": "failed", "error": str(result.result)})

    return JsonResponse({"status": result.state})


@api_view(["GET"])
@permission_classes([AllowAny])
def download_file(request, task_id):

    result = AsyncResult(task_id, app=app)

    if result.state != "SUCCESS":
        return JsonResponse({"error": "File not ready"}, status=400)

    data = result.result or {}
    file_url = data.get("file_url")

    if not file_url:
        return JsonResponse({"error": "Missing file_url"}, status=500)

    return JsonResponse({"download_url": file_url})


@api_view(["GET"])
@permission_classes([AllowAny])
def upload_stats(request):
    stats = UploadStats.objects.first()
    if not stats:
        stats = UploadStats.objects.create()

    return JsonResponse(
        {
            "total_files_processed": stats.total_files_processed,
            "total_storage_processed_bytes": stats.total_storage_processed,
            "total_storage_processed_mb": bytes_to_mb(stats.total_storage_processed),
            "total_storage_processed_gb": bytes_to_gb(stats.total_storage_processed),
        }
    )
