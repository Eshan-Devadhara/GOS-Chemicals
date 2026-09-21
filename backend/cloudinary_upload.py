"""Cloudinary upload helper for production image storage.

When Cloudinary environment variables are configured, uploads go to
Cloudinary and a public URL is returned.  When they are not configured
(local dev), returns None so the caller can fall back to local file storage.
"""

import os


def _get_cloudinary_config():
    """Return True if Cloudinary is fully configured, False otherwise."""
    cloud_name = os.getenv('CLOUDINARY_CLOUD_NAME')
    api_key = os.getenv('CLOUDINARY_API_KEY')
    api_secret = os.getenv('CLOUDINARY_API_SECRET')
    return bool(cloud_name and api_key and api_secret)


def _configure_cloudinary():
    """Configure the cloudinary SDK from environment variables."""
    import cloudinary
    cloudinary.config(
        cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
        api_key=os.getenv('CLOUDINARY_API_KEY'),
        api_secret=os.getenv('CLOUDINARY_API_SECRET'),
        secure=True,
    )


def upload_image(file_obj, original_filename):
    """Upload *file_obj* to Cloudinary and return (url, public_id).

    Returns ``(None, None)`` if Cloudinary is not configured so the caller
    can fall back to local storage.
    """
    if not _get_cloudinary_config():
        return None, None

    try:
        import cloudinary.uploader
    except ImportError:
        return None, None

    _configure_cloudinary()

    from werkzeug.utils import secure_filename
    safe_name = secure_filename(original_filename)
    # Strip extension for the public_id
    name_part = os.path.splitext(safe_name)[0]

    result = cloudinary.uploader.upload(
        file_obj,
        folder='gos_chemicals',
        public_id=name_part,
        unique_filename=True,
        overwrite=False,
        resource_type='image',
    )

    return result.get('secure_url'), result.get('public_id')


def delete_image(public_id):
    """Delete an image from Cloudinary by its public_id.

    Returns True on success, False if Cloudinary is not configured or
    deletion fails.
    """
    if not public_id or not _get_cloudinary_config():
        return False

    try:
        import cloudinary.uploader
    except ImportError:
        return False

    _configure_cloudinary()

    try:
        result = cloudinary.uploader.destroy(public_id)
        return result.get('result') == 'ok'
    except Exception:
        return False
