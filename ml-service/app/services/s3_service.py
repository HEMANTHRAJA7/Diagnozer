import os
import uuid
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
    return f"http://localhost:8000/{settings.LOCAL_UPLOAD_DIR}/{filename}"

def upload_image_to_s3(file_bytes: bytes, filename: str, content_type: str = "image/jpeg") -> str:
    if settings.MOCK_S3_UPLOAD:
        return save_image_mock(file_bytes, filename)
    
    # TODO: Actual boto3 logic will go here when MOCK_S3_UPLOAD is False
    print("Warning: Actual S3 Upload Not Implemented Yet!")
    return ""

def upload_heatmap_to_s3(file_bytes: bytes, filename: str) -> str:
    if settings.MOCK_S3_UPLOAD:
        return save_image_mock(file_bytes, filename, prefix="heatmap")
        
    # TODO: Actual boto3 logic will go here
    return ""
