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

        import io
        from PIL import Image
        from tensorflow.keras.applications.efficientnet import preprocess_input

        if not self.stage_a:
            raise FileNotFoundError(
                f"Stage A Model not found at {MODEL_A_PATH}"
            )

        IMG_SIZE = (300, 300)

        # Image Preprocessing (matching user's notebook)
        image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
        image = image.resize(IMG_SIZE)

        image_array = np.array(image).astype("float32")

        # Keep a clean [0,1] copy for SHAP heatmap display
        display_image = image_array / 255.0

        image_array = np.expand_dims(image_array, axis=0)
        image_array = preprocess_input(image_array)

        # Stage A Prediction (Fruit / Leaf)
        preds_a = self.stage_a.predict(image_array)[0]

        stage_a_index = int(np.argmax(preds_a))
        stage_a_conf = float(np.max(preds_a))

        if stage_a_conf >= 0.5:
            stage_a_label = "Fruit"
            active_model = self.stage_b_fruit
            active_labels = self.labels_b_fruit
        else:
            stage_a_label = "Leaf"
            active_model = self.stage_b_leaf
            active_labels = self.labels_b_leaf

        stage = "B1 (Fruit Model)" if stage_a_label == "Fruit" else "B2 (Leaf Model)"

        if not active_model:
            raise RuntimeError(
                f"Missing Stage B model for parsed type: {stage_a_label}"
            )

        # Stage B Prediction
        preds_b = active_model.predict(image_array)[0]

        idx_b = int(np.argmax(preds_b))
        confidence = float(np.max(preds_b))

        class_name = active_labels.get(
            str(idx_b),
            f"{stage_a_label}_Class_{idx_b}"
        )

        class_probabilities = preds_b.tolist()

        # Keep original expected keys for backwards compatibility in the system if needed, 
        # but also provide the exact JSON structure the user asked for.
        return {
            # User defined fields
            "stageA_prediction": stage_a_label,
            "stageA_confidence": round(stage_a_conf, 4),
            "finalPrediction": class_name,
            "confidence": round(confidence, 4),
            "classProbabilities": class_probabilities,
            "modelUsed": stage,
            
            # Additional API fields that might be expected
            "predictedClass": class_name,
            "predictedClassIndex": idx_b,
            "imageType": stage_a_label,
            "active_model_wrapper": active_model,
            "active_tensor": image_array,
            "display_image": display_image
        }

jackfruit_predictor = JackfruitPredictor()