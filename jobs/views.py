import os
import tempfile
from core.celery import app
from celery.result import AsyncResult
from django.http import JsonResponse
from django.http import HttpResponse, FileResponse
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from .tasks import inspect_file_task, convert_to_geopackage_task


@api_view(["POST"])
@permission_classes([AllowAny])
def inspect_file(request):

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return HttpResponse("No file uploaded", status=400)

    original_name = uploaded_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp:
        for chunk in uploaded_file.chunks():
            temp.write(chunk)
        temp_path = temp.name

    task = inspect_file_task.delay(temp_path, original_name)

    return JsonResponse(
        {"message": "Processing started", "task_id": task.id}, status=202
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def convert_to_geopackage(request):

    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return HttpResponse("No file uploaded", status=400)

    original_name = uploaded_file.name
    base_name = os.path.splitext(original_name)[0]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp:
        for chunk in uploaded_file.chunks():
            temp.write(chunk)
        temp_path = temp.name

    task = convert_to_geopackage_task.delay(temp_path, base_name)

    return JsonResponse(
        {"message": "Processing started", "task_id": task.id}, status=202
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def task_status(request, task_id):

    result = AsyncResult(task_id, app=app)

    if result.state == "PENDING":
        return JsonResponse({"status": "pending"})

    elif result.state == "SUCCESS":
        return JsonResponse({"status": "done", "data": result.result})

    elif result.state == "FAILURE":
        return JsonResponse({"status": "failed"})

    return JsonResponse({"status": result.state})
