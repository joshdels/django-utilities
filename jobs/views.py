import os
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, FileResponse
import tempfile

from .services.dxf_inspect import run_inspection
from .services.dxf_extract import extract_to_geopackage


@api_view(["POST"])
@permission_classes([AllowAny])
def inspect_file(request):
    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return HttpResponse("No file uploaded", status=400)

    original_name = uploaded_file.name

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp:
        temp.write(uploaded_file.read())
        temp_path = temp.name

    try:
        report_text = run_inspection(temp_path, original_name)

        response = HttpResponse(report_text, content_type="text/plain")
        response["Content-Disposition"] = 'attachment; filename="report.txt"'

        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)


@api_view(["POST"])
@permission_classes([AllowAny])
def convert_to_geopackage(request):
    uploaded_file = request.FILES.get("file")

    if not uploaded_file:
        return HttpResponse("No file uploaded", status=400)

    original_name = uploaded_file.name
    base_name = os.path.splitext(original_name)[0]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".dxf") as temp_dxf:
        temp_dxf.write(uploaded_file.read())
        temp_dxf_path = temp_dxf.name

    temp_gpkg = tempfile.NamedTemporaryFile(delete=False, suffix=".gpkg")
    temp_gpkg_path = temp_gpkg.name
    temp_gpkg.close()

    try:
        output_path = extract_to_geopackage(
            file_path=temp_dxf_path, output_path=temp_gpkg_path
        )

        if not output_path or not os.path.exists(output_path):
            return HttpResponse("Conversion failed", status=500)

        response = FileResponse(
            open(output_path, "rb"), content_type="application/geopackage+sqlite3"
        )

        response["Content-Disposition"] = f'attachment; filename="{base_name}.gpkg"'

        return response

    except Exception as e:
        return HttpResponse(f"Error: {str(e)}", status=500)

    finally:
        if os.path.exists(temp_dxf_path):
            os.remove(temp_dxf_path)
