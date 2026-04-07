from fastapi import APIRouter

router = APIRouter()

@router.get("/health", tags=["health"])
async def check_health():
    """Check the health status of the ML Service."""
    return {"status": "ok", "message": "Diagnozer ML Service is running smoothly!"}
