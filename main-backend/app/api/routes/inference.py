from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, Form
import httpx
from typing import Optional
from app.api.dependencies import get_current_user
from app.db.mongodb import get_database
from app.core.config import settings
from app.models.history import PredictionHistory

router = APIRouter()

@router.post("/")
async def proxy_predict(
    crop: str = Form(...), # 'mango' or 'jackfruit'
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db=Depends(get_database)
):
    """
    Proxies an image upload to the ML Service, then saves the result to MongoDB.
    """
    if crop not in ["mango", "jackfruit"]:
        raise HTTPException(status_code=400, detail="Crop must be 'mango' or 'jackfruit'")
        
    file_bytes = await file.read()
    
    # Send directly to ML service
    ml_url = f"{settings.ML_SERVICE_URL}/api/v1/predict/{crop}"
    
    async with httpx.AsyncClient() as client:
        try:
            # We must forward it accurately
            files = {"file": (file.filename, file_bytes, file.content_type)}
            response = await client.post(ml_url, files=files, timeout=300.0)
            
            if response.status_code != 200:
                print(f"ML Service Error: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="ML Service Error")
                
            prediction_data = response.json()
            
            # Save mapping to MongoDB history array
            history_record = PredictionHistory(
                user_id=str(current_user["_id"]),
                crop_type=crop,
                image_type=prediction_data.get("imageType"),
                predicted_class=prediction_data["predictedClass"],
                confidence=prediction_data["confidence"],
                heatmap_url=prediction_data["heatmapUrl"],
                explanation=prediction_data.get("explanation")
            )
            await db["history"].insert_one(history_record.dict())
            
            return prediction_data
            
        except httpx.RequestError as e:
            print(f"Connection error to ML Service: {e}")
            raise HTTPException(status_code=503, detail="ML Service Unavailable")
