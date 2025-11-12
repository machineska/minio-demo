from django.db import models

class EventLog(models.Model):
    event_type = models.CharField(max_length=64)
    object_key = models.CharField(max_length=1024)
    etag = models.CharField(max_length=128, blank=True)
    version_id = models.CharField(max_length=256, blank=True)
    occurred_at = models.DateTimeField()
    payload = models.JSONField()

    class Meta:
        ordering = ["-occurred_at"]
