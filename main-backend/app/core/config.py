import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Diagnozer Main Backend"
    VERSION: str = "1.0.0"
    
    # DB Configuration
    MONGODB_URL: str = "mongodb://localhost:27017" # Default for local dev, overriden in Atlas
    DB_NAME: str = "diagnozer_db"
    
    # Auth Security
    SECRET_KEY: str = "super_secret_dev_key_change_in_production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30 * 24 * 60 # 30 days default
    
    # Proxy Config
    ML_SERVICE_URL: str = "http://localhost:8000"
    
    # Generative AI Config
    GEMINI_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
