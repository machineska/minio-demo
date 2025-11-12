from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EventLog",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("event_type", models.CharField(max_length=64)),
                ("object_key", models.CharField(max_length=1024)),
                ("etag", models.CharField(blank=True, max_length=128)),
                ("version_id", models.CharField(blank=True, max_length=256)),
                ("occurred_at", models.DateTimeField()),
                ("payload", models.JSONField()),
            ],
            options={"ordering": ["-occurred_at"]},
        ),
    ]
