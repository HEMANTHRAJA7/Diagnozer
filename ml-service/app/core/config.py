import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Diagnozer ML Service"
    VERSION: str = "1.0.0"
    
    # S3 config
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    S3_BUCKET_NAME: str = ""
    AWS_REGION: str = "us-east-1"
    
    # Mock behavior flag
    MOCK_S3_UPLOAD: bool = True  # Set to True to save images locally instead
    LOCAL_UPLOAD_DIR: str = "uploads"

    class Config:
        env_file = ".env"

settings = Settings()
