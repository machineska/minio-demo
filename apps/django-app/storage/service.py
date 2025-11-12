import os
from django.conf import settings
from minio import Minio
from minio.commonconfig import CopySource

def get_client():
    endpoint = settings.MINIO_ENDPOINT.replace("http://", "").replace("https://", "")
    secure = settings.MINIO_ENDPOINT.startswith("https://")
    return Minio(
        endpoint,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=secure,
        region=settings.MINIO_REGION,
    )

def put_object(client, bucket, object_name, file_obj, size, content_type):
    client.put_object(bucket, object_name, file_obj, size, content_type=content_type)

def list_objects(client, bucket):
    return client.list_objects(bucket, recursive=True)

def presigned_get(client, bucket, object_name, expiry):
    return client.get_presigned_url("GET", bucket, object_name, expires=expiry)

def remove_object(client, bucket, object_name, version_id=None):
    client.remove_object(bucket, object_name, version_id=version_id)

def list_versions(client, bucket, prefix):
    return client.list_objects(bucket, prefix=prefix, recursive=True, include_version=True)

def restore_version(client, bucket, object_name, version_id):
    src = CopySource(bucket, object_name, version_id=version_id)
    client.copy_object(bucket, object_name, src)

def ensure_bucket(client, bucket, region):
    exists = client.bucket_exists(bucket)
    if not exists:
        client.make_bucket(bucket, location=region)
