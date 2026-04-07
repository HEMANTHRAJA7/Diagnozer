import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import health, mango, jackfruit
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="ML Inference service for Diagnozer App"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure local upload directory exists for mocked images
if not os.path.exists(settings.LOCAL_UPLOAD_DIR):
    os.makedirs(settings.LOCAL_UPLOAD_DIR)

# Mount the static directory so mocked S3 image URLs actually resolve across local test devices
app.mount(f"/{settings.LOCAL_UPLOAD_DIR}", StaticFiles(directory=settings.LOCAL_UPLOAD_DIR), name="uploads")

app.include_router(health.router, prefix="/api/v1")
app.include_router(mango.router, prefix="/api/v1/predict")
app.include_router(jackfruit.router, prefix="/api/v1/predict")
