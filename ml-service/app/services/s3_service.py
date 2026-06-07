import os
import uuid
import boto3
from app.core.config import settings

def save_image_mock(file_bytes: bytes, original_filename: str, prefix: str = "raw") -> str:
    """Mock saving to S3 by saving locally to disk."""
    if not os.path.exists(settings.LOCAL_UPLOAD_DIR):
        os.makedirs(settings.LOCAL_UPLOAD_DIR)
        
    ext = original_filename.split(".")[-1]
    filename = f"{prefix}_{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join(settings.LOCAL_UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as f:
        f.write(file_bytes)
        
    # Return a mock URL
    # In production, this would be a real S3 URL
    return f"{settings.ML_SERVICE_EXTERNAL_URL}/{settings.LOCAL_UPLOAD_DIR}/{filename}"

def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION
    )

def upload_image_to_s3(file_bytes: bytes, filename: str, content_type: str = "image/jpeg") -> str:
    if settings.MOCK_S3_UPLOAD:
        return save_image_mock(file_bytes, filename)
    
    ext = filename.split(".")[-1] if "." in filename else "jpg"
    s3_key = f"raw/{uuid.uuid4().hex}.{ext}"
    
    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType=content_type
        )
        return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
    except Exception as e:
        print(f"Error uploading image to S3: {e}")
        raise e

def upload_heatmap_to_s3(file_bytes: bytes, filename: str) -> str:
    if settings.MOCK_S3_UPLOAD:
        return save_image_mock(file_bytes, filename, prefix="heatmap")
        
    ext = filename.split(".")[-1] if "." in filename else "png"
    s3_key = f"heatmaps/{uuid.uuid4().hex}.{ext}"
    
    try:
        s3 = get_s3_client()
        s3.put_object(
            Bucket=settings.S3_BUCKET_NAME,
            Key=s3_key,
            Body=file_bytes,
            ContentType="image/png"
        )
        return f"https://{settings.S3_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"
    except Exception as e:
        print(f"Error uploading heatmap to S3: {e}")
        raise e

