import os
import uuid
from typing import Optional

import aiofiles
import aioboto3

from app.core.config import settings


async def save_image_locally(file_bytes: bytes, filename: str) -> str:
    uploads_dir = os.path.join(os.getcwd(), 'static', 'uploads')
    os.makedirs(uploads_dir, exist_ok=True)
    # create a unique filename
    ext = os.path.splitext(filename)[1] or '.jpg'
    key = f"{uuid.uuid4().hex}{ext}"
    path = os.path.join(uploads_dir, key)
    async with aiofiles.open(path, 'wb') as f:
        await f.write(file_bytes)
    # Return path relative to server root — caller should build full URL if needed
    return f"/static/uploads/{key}"


async def save_image_to_s3(file_bytes: bytes, filename: str) -> str:
    # Use aioboto3 to upload and return public URL
    if not settings.s3_bucket:
        raise RuntimeError('S3 bucket is not configured')

    ext = os.path.splitext(filename)[1] or '.jpg'
    key = f"{uuid.uuid4().hex}{ext}"

    session = aioboto3.Session()
    async with session.client(
        's3',
        region_name=settings.s3_region or None,
        aws_access_key_id=settings.s3_access_key_id or None,
        aws_secret_access_key=settings.s3_secret_access_key or None,
        endpoint_url=settings.s3_endpoint_url or None,
    ) as client:
        await client.put_object(Bucket=settings.s3_bucket, Key=key, Body=file_bytes, ACL='public-read', ContentType='image/jpeg')

    # Construct public URL
    if settings.s3_public_url:
        return f"{settings.s3_public_url.rstrip('/')}/{key}"

    if settings.s3_endpoint_url:
        # endpoint like https://<region>.digitaloceanspaces.com -> bucket/key
        return f"{settings.s3_endpoint_url.rstrip('/')}/{settings.s3_bucket}/{key}"

    # default AWS S3 public URL
    region = settings.s3_region
    return f"https://{settings.s3_bucket}.s3.{region}.amazonaws.com/{key}"


async def save_image(file_bytes: bytes, filename: str) -> str:
    """Save image using S3 if enabled, otherwise save locally and return accessible path/URL."""
    if settings.s3_enabled:
        return await save_image_to_s3(file_bytes, filename)
    else:
        return await save_image_locally(file_bytes, filename)
