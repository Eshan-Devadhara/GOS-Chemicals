"""S3 upload helper for production image storage.

When AWS credentials are configured, uploads go to S3 and a public URL is
returned.  When they are not configured (local dev), returns None so the
caller can fall back to local file storage.
"""

import os
import uuid

_s3_client = None


def _get_s3_client():
    """Lazy-init boto3 S3 client.  Returns None if credentials are missing."""
    global _s3_client
    if _s3_client is not None:
        return _s3_client

    try:
        import boto3
    except ImportError:
        return None

    key_id = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')
    region = os.getenv('AWS_REGION', 'us-east-1')

    if not (key_id and secret):
        return None

    _s3_client = boto3.client(
        's3',
        aws_access_key_id=key_id,
        aws_secret_access_key=secret,
        region_name=region,
    )
    return _s3_client


def upload_to_s3(file_obj, original_filename, content_type=None):
    """Upload *file_obj* to S3 and return the public URL.

    Returns ``None`` if S3 is not configured so the caller can fall back
    to local storage.
    """
    client = _get_s3_client()
    bucket = os.getenv('AWS_S3_BUCKET')
    region = os.getenv('AWS_REGION', 'us-east-1')

    if client is None or not bucket:
        return None

    from werkzeug.utils import secure_filename

    safe_name = secure_filename(original_filename)
    key = f"uploads/{uuid.uuid4().hex}_{safe_name}"

    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type

    client.upload_fileobj(
        file_obj,
        bucket,
        key,
        ExtraArgs=extra_args,
    )

    url = f"https://{bucket}.s3.{region}.amazonaws.com/{key}"
    return url
