import io
import json
from datetime import datetime
from django.conf import settings
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import EventLog
from .service import get_client, put_object, list_objects, presigned_get, remove_object, list_versions, restore_version, ensure_bucket

def index(request):
    return render(request, "upload.html")

def upload(request):
    if request.method == "POST" and request.FILES.get("file"):
        f = request.FILES["file"]
        client = get_client()
        ensure_bucket(client, settings.MINIO_BUCKET, settings.MINIO_REGION)
        put_object(client, settings.MINIO_BUCKET, f.name, f.file, f.size, f.content_type or "application/octet-stream")
        return HttpResponseRedirect(reverse("list"))
    return render(request, "upload.html")

def list_view(request):
    client = get_client()
    ensure_bucket(client, settings.MINIO_BUCKET, settings.MINIO_REGION)
    objs = list(list_objects(client, settings.MINIO_BUCKET))
    context = {"objects": objs}
    return render(request, "list.html", context)

def presign(request, key):
    client = get_client()
    url = presigned_get(client, settings.MINIO_BUCKET, key, settings.PRESIGN_TTL)
    return JsonResponse({"url": url})

def delete(request, key):
    client = get_client()
    remove_object(client, settings.MINIO_BUCKET, key)
    return HttpResponseRedirect(reverse("list"))

def versions(request, key):
    client = get_client()
    versions_iter = list_versions(client, settings.MINIO_BUCKET, key)
    items = []
    for v in versions_iter:
        if hasattr(v, "is_latest"):
            items.append({
                "version_id": v.version_id,
                "is_latest": v.is_latest,
                "size": getattr(v, "size", None),
                "etag": getattr(v, "etag", ""),
                "last_modified": getattr(v, "last_modified", None),
                "key": v.object_name,
            })
    return render(request, "versions.html", {"key": key, "versions": items})

def restore(request, key, version_id):
    client = get_client()
    restore_version(client, settings.MINIO_BUCKET, key, version_id)
    return HttpResponseRedirect(reverse("versions", args=[key]))

@csrf_exempt
def events_webhook(request):
    if request.method != "POST":
        return JsonResponse({"status": "method_not_allowed"}, status=405)
    payload = json.loads(request.body.decode("utf-8"))
    records = payload.get("Records", [])
    for r in records:
        event_name = r.get("eventName", "")
        key = r.get("s3", {}).get("object", {}).get("key", "")
        etag = r.get("s3", {}).get("object", {}).get("eTag", "")
        version_id = r.get("s3", {}).get("object", {}).get("versionId", "")
        event_time = r.get("eventTime", datetime.utcnow().isoformat())
        occurred_at = datetime.fromisoformat(event_time.replace("Z", "+00:00"))
        EventLog.objects.create(event_type=event_name, object_key=key, etag=etag, version_id=version_id, occurred_at=occurred_at, payload=r)
    return JsonResponse({"status": "ok"})

def events_view(request):
    logs = EventLog.objects.all()[:200]
    return render(request, "events.html", {"logs": logs})
