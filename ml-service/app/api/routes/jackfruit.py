from fastapi import APIRouter, File, UploadFile, HTTPException
import traceback
from app.schemas.prediction import PredictionResponse
from app.services.s3_service import upload_image_to_s3, upload_heatmap_to_s3
from app.ml.tflite_utils import preprocess_image
from app.ml.jackfruit_model import jackfruit_predictor
from app.ml.shap_explainer import generate_shap_heatmap

router = APIRouter()

@router.post("/jackfruit", response_model=PredictionResponse, tags=["jackfruit"])
async def predict_jackfruit_route(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    file_bytes = await file.read()
    raw_image_url = upload_image_to_s3(file_bytes, file.filename, file.content_type)
    
    try:
        # Multistage Pipeline Invocation passes raw bytes natively
        prediction_result = jackfruit_predictor.predict(file_bytes)
        active_model_wrapper = prediction_result.pop("active_model_wrapper")
        active_tensor = prediction_result.pop("active_tensor")
        display_image = prediction_result.pop("display_image", None)
        
        # SHAP calculation over the specific Stage B model used
        heatmap_bytes = generate_shap_heatmap(active_model_wrapper, active_tensor, display_image=display_image)
        heatmap_url = upload_heatmap_to_s3(heatmap_bytes, "heatmap.png")
        
        return PredictionResponse(
            predictedClass=prediction_result["predictedClass"],
            confidence=prediction_result["confidence"],
            classProbabilities=prediction_result["classProbabilities"],
            predictedClassIndex=prediction_result["predictedClassIndex"],
            heatmapUrl=heatmap_url,
            explanation=f"SHAP localizes features matching {prediction_result['predictedClass']} on your {prediction_result['imageType']} capture.",
            imageType=prediction_result["imageType"]
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
