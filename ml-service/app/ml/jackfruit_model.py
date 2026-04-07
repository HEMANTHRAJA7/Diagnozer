import os
import numpy as np
from app.ml.tflite_utils import TFLiteModelWrapper, load_labels

MODEL_A_PATH = "models/StageA_Fruit_vs_Leaf_float16.tflite"
LABELS_A_PATH = "models/class_names_jackfruit_stageA.json"

MODEL_B_FRUIT_PATH = "models/StageB_Fruit_float16.tflite"
LABELS_B_FRUIT_PATH = "models/class_names_jackfruit_stageB_fruit.json"

MODEL_B_LEAF_PATH = "models/StageB_Leaf_float16.tflite"
LABELS_B_LEAF_PATH = "models/class_names_jackfruit_stageB_leaf.json"

class JackfruitPredictor:
    def __init__(self):
        self.stage_a = None
        self.stage_b_fruit = None
        self.stage_b_leaf = None
        
        self.labels_a = {}
        self.labels_b_fruit = {}
        self.labels_b_leaf = {}
        
    def load(self):
        if self.stage_a is None and os.path.exists(MODEL_A_PATH):
            self.stage_a = TFLiteModelWrapper(MODEL_A_PATH)
            self.labels_a = load_labels(LABELS_A_PATH)
            
        if self.stage_b_fruit is None and os.path.exists(MODEL_B_FRUIT_PATH):
            self.stage_b_fruit = TFLiteModelWrapper(MODEL_B_FRUIT_PATH)
            self.labels_b_fruit = load_labels(LABELS_B_FRUIT_PATH)
            
        if self.stage_b_leaf is None and os.path.exists(MODEL_B_LEAF_PATH):
            self.stage_b_leaf = TFLiteModelWrapper(MODEL_B_LEAF_PATH)
            self.labels_b_leaf = load_labels(LABELS_B_LEAF_PATH)

    def predict(self, file_bytes: bytes):
        self.load()
        from app.ml.tflite_utils import preprocess_image
        if not self.stage_a:
            raise FileNotFoundError(f"Stage A Model not found at {MODEL_A_PATH}")

        # Stage A (requires 300x300)
        shape_a = self.stage_a.input_details[0]['shape']
        tensor_a = preprocess_image(file_bytes, target_size=(int(shape_a[1]), int(shape_a[2])))
        
        preds_a = self.stage_a.predict(tensor_a)[0]
        idx_a = np.argmax(preds_a)
        image_type = self.labels_a.get(str(idx_a), "Unknown")
        
        active_model = None
        active_labels = {}
        
        if image_type == "Fruit" and self.stage_b_fruit:
            active_model = self.stage_b_fruit
            active_labels = self.labels_b_fruit
        elif image_type == "Leaf" and self.stage_b_leaf:
            active_model = self.stage_b_leaf
            active_labels = self.labels_b_leaf
        else:
            raise RuntimeError(f"Missing Stage B model for parsed type: {image_type}")

        # Stage B (might require 224x224 or 300x300 dynamically)
        shape_b = active_model.input_details[0]['shape']
        tensor_b = preprocess_image(file_bytes, target_size=(int(shape_b[1]), int(shape_b[2])))
        
        preds_b = active_model.predict(tensor_b)[0]
        idx_b = np.argmax(preds_b)
        confidence = float(preds_b[idx_b])
        class_name = active_labels.get(str(idx_b), f"{image_type}_Class_{idx_b}")

        return {
            "predictedClass": class_name,
            "confidence": confidence,
            "classProbabilities": preds_b.tolist(),
            "predictedClassIndex": int(idx_b),
            "imageType": image_type,
            "active_model_wrapper": active_model, # Passed back for SHAP generator
            "active_tensor": tensor_b
        }
        
jackfruit_predictor = JackfruitPredictor()
