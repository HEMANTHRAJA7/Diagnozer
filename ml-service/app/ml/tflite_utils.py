import numpy as np
from PIL import Image, ImageOps
import io
import json

def preprocess_image(file_bytes: bytes, target_size: tuple = (224, 224)) -> np.ndarray:
    """
    Preprocess the incoming image bytes for TFLite float16/float32 ingestion.
    Uses padding to maintain exact aspect ratio without skewing the disease patterns.
    """
    image = Image.open(io.BytesIO(file_bytes)).convert("RGB")
    
    # Pad to make it a square before resizing, maintaining aspect ratio
    image = ImageOps.pad(image, target_size, method=Image.LANCZOS, color=(0, 0, 0))
    
    # Convert to array and normalize
    # Many tflite floats expect 0..1 scale. If specific models want 0..255, adjust here.
    img_array = np.array(image, dtype=np.float32) / 255.0
    
    # Add batch dimension: output shape (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def load_labels(filepath: str) -> dict:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return {}

class TFLiteModelWrapper:
    """Wrapper to handle TFLite Interpreter initialization and invocations."""
    def __init__(self, model_path: str):
        try:
            import ai_edge_litert.interpreter as tflite
            self.interpreter = tflite.Interpreter(model_path=model_path)
        except ImportError:
            try:
                import tflite_runtime.interpreter as tflite
                self.interpreter = tflite.Interpreter(model_path=model_path)
            except ImportError:
                # Fallback for local testing if ai_edge_litert is unavailable
                import tensorflow as tf
                self.interpreter = tf.lite.Interpreter(model_path=model_path)
            
        self.interpreter.allocate_tensors()
        self.input_details = self.interpreter.get_input_details()
        self.output_details = self.interpreter.get_output_details()
        
    def predict(self, input_tensor: np.ndarray) -> np.ndarray:
        # Cast to expected type (usually FLOAT32 even if model internals are FLOAT16)
        input_type = self.input_details[0]['dtype']
        if input_tensor.dtype != input_type:
            input_tensor = input_tensor.astype(input_type)
            
        self.interpreter.set_tensor(self.input_details[0]['index'], input_tensor)
        self.interpreter.invoke()
        output_data = self.interpreter.get_tensor(self.output_details[0]['index'])
        return output_data
