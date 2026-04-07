import os
import numpy as np
from app.ml.tflite_utils import TFLiteModelWrapper, load_labels

# Path relative to the working directory where the script runs
MODEL_PATH = "models/mango_dynamic_range.tflite"
LABELS_PATH = "models/class_names_mango.json"

# Singleton instance
class MangoPredictor:
    def __init__(self):
        self.model = None
        self.labels = {}
        
    def load(self):
        if self.model is None and os.path.exists(MODEL_PATH):
            self.model = TFLiteModelWrapper(MODEL_PATH)
            self.labels = load_labels(LABELS_PATH)
            
    def predict(self, input_tensor: np.ndarray):
        self.load()
        if not self.model:
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
            
        preds = self.model.predict(input_tensor)[0]
        class_idx = np.argmax(preds)
        confidence = float(preds[class_idx])
        
        # Determine class name
        class_name = self.labels.get(str(class_idx), f"Class_{class_idx}")
        
        return {
            "predictedClass": class_name,
            "confidence": confidence,
            "classProbabilities": preds.tolist(),
            "predictedClassIndex": int(class_idx)
        }
        
mango_predictor = MangoPredictor()
