import boto3
from django.conf import settings

def generate_presigned_url(key, expires_in=3600):
    """
    Generate a pre-signed URL to access a file in MinIO for a limited time (default: 1 hour).
    """
    s3_client = boto3.client(
        's3',
        endpoint_url=settings.AWS_S3_ENDPOINT_URL,
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
    return s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME, 'Key': key},
        ExpiresIn=expires_in
    )
