from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.mongodb import connect_to_mongo, close_mongo_connection
from app.api.routes import auth, inference, chat

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Primary API Gateway, User Profiles, Auth, and Chatbot for Diagnozer."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/api/v1/health", tags=["health"])
async def check_health():
    return {"status": "ok", "message": "Diagnozer Main Backend API is live."}

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(inference.router, prefix="/api/v1/inference", tags=["Inference"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])
