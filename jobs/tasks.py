import os
import uuid
import time
import zipfile
from celery import shared_task
from .services.dxf_inspect import run_inspection
from .services.dxf_extract import extract_to_geopackage
from core.utils.storage import upload_file_to_b2

MEDIA_DIR = "/app/media/tmp"


@shared_task(bind=True)
def process_dxf_task(self, temp_path, original_name):

    report_path = None
    gpkg_path = None
    zip_path = None

    try:
        task_id = self.request.id
        os.makedirs(MEDIA_DIR, exist_ok=True)

        # ----------------------------
        # STEP 1: INSPECTION
        # ----------------------------
        self.update_state(state="PROGRESS", meta={"step": "Inspecting DXF"})
        report_text = run_inspection(temp_path, original_name)

        if not report_text:
            raise ValueError("Inspection failed")

        report_path = f"{MEDIA_DIR}/{task_id}_report.txt"
        with open(report_path, "w") as f:
            f.write(report_text)

        # ----------------------------
        # STEP 2: CONVERSION
        # ----------------------------
        self.update_state(state="PROGRESS", meta={"step": "Converting to GPKG"})
        gpkg_path = f"{MEDIA_DIR}/{task_id}.gpkg"

        result_path = extract_to_geopackage(temp_path, gpkg_path)

        if not result_path:
            raise ValueError("Conversion failed")

        # ----------------------------
        # STEP 3: ZIP
        # ----------------------------
        self.update_state(state="PROGRESS", meta={"step": "Packaging ZIP"})
        zip_path = f"{MEDIA_DIR}/{task_id}.zip"

        with zipfile.ZipFile(zip_path, "w") as zipf:
            zipf.write(report_path, os.path.basename(report_path))
            zipf.write(gpkg_path, os.path.basename(gpkg_path))

        # ----------------------------
        # STEP 4: CLOUD UPLOAD
        # ----------------------------

        remote_path = f"processed/{task_id}.zip"
        file_url = upload_file_to_b2(zip_path, remote_path)

        return {"task_id": task_id, "file_url": file_url}

    except Exception as e:
        raise RuntimeError(str(e))

    finally:
        for f in [temp_path, report_path, gpkg_path, zip_path]:
            if f and os.path.exists(f):
                os.remove(f)


@shared_task
def cleanup_old_files(hours=24):

    now = time.time()
    cutoff = now - (hours * 3600)

    deleted = 0

    for filename in os.listdir(MEDIA_DIR):
        path = os.path.join(MEDIA_DIR, filename)

        if os.path.isfile(path):
            if os.path.getmtime(path) < cutoff:
                os.remove(path)
                deleted += 1

    return {"deleted_files": deleted}
