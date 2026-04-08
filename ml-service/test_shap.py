import os
import sys
import numpy as np
import io
from PIL import Image

# Add ml-service path
sys.path.append(os.path.abspath('.'))

from app.ml.mango_model import mango_predictor
from app.ml.tflite_utils import preprocess_image
from app.ml.shap_explainer import generate_shap_heatmap

def run_test():
    print("Loading model...")
    mango_predictor.load()
    
    # Create fake image
    print("Creating fake 240x240 image...")
    b = io.BytesIO()
    Image.new('RGB', (240, 240)).save(b, 'JPEG')
    b.seek(0)
    
    # Get shape
    shape = mango_predictor.model.input_details[0]['shape']
    print(f"Model expects shape: {shape}")
    
    # Preprocess
    arr = preprocess_image(b.read(), target_size=(int(shape[1]), int(shape[2])))
    print(f"Preprocessed array shape: {arr.shape}")
    
    # SHAP
    print("Starting SHAP generation (this might hang or crash)...")
    try:
        res = generate_shap_heatmap(mango_predictor.model, arr)
        print(f"SHAP SUCCESS! Heatmap byte size: {len(res)}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"SHAP ERROR: {e}")

if __name__ == '__main__':
    run_test()
