from fastapi import APIRouter, File, UploadFile, HTTPException
import traceback
from app.schemas.prediction import PredictionResponse
from app.services.s3_service import upload_image_to_s3, upload_heatmap_to_s3
from app.ml.tflite_utils import preprocess_image
from app.ml.mango_model import mango_predictor
from app.ml.shap_explainer import generate_shap_heatmap

router = APIRouter()

@router.post("/mango", response_model=PredictionResponse, tags=["mango"])
async def predict_mango_route(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File provided is not an image.")
    
    file_bytes = await file.read()
    raw_image_url = upload_image_to_s3(file_bytes, file.filename, file.content_type)
    
    try:
        # Load model first to dynamically get its required input dimensions
        mango_predictor.load()
        target_height = mango_predictor.model.input_details[0]['shape'][1]
        target_width = mango_predictor.model.input_details[0]['shape'][2]
        
        # Preprocess dynamically
        input_tensor = preprocess_image(file_bytes, target_size=(int(target_height), int(target_width)))
        
        # Model invocation
        prediction_result = mango_predictor.predict(input_tensor)
        
        # SHAP calculation
        heatmap_bytes = generate_shap_heatmap(mango_predictor.model, input_tensor)
        heatmap_url = upload_heatmap_to_s3(heatmap_bytes, "heatmap.png")
        
        return PredictionResponse(
            predictedClass=prediction_result["predictedClass"],
            confidence=prediction_result["confidence"],
            classProbabilities=prediction_result["classProbabilities"],
            predictedClassIndex=prediction_result["predictedClassIndex"],
            heatmapUrl=heatmap_url,
            explanation=f"SHAP attribution mapping localized critical features for {prediction_result['predictedClass']}."
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
