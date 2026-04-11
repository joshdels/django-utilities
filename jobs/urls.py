from django.urls import path
from .views import process_dxf, task_status, download_file

urlpatterns = [
    path("process-dxf/", process_dxf),
    path("task-status/<str:task_id>/", task_status),
    path("download/<str:task_id>/", download_file),
]
