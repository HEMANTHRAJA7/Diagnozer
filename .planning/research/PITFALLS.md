# Pitfalls Research: Agriculture Disease Detection App

## Common Mistakes in this Domain

### 1. SHAP Computation Latency
- **Warning Sign:** The ML prediction API takes 5-15 seconds to return. 
- **Prevention Strategy:** SHAP (KernelShap/DeepExplainer) can be incredibly slow on high-resolution images because it perturbs the image hundreds of times. Use specifically tuned `GradientExplainer` or limit the background dataset size for the SHAP explainer to achieve sub-second generation.
- **Phase:** Addressed during early ML Service implementation.

### 2. TFLite Float16 Compatibility in Python
- **Warning Sign:** Discrepancies between TF model training outputs and TFLite production outputs, or generic `interpreter.invoke()` crashing without descriptive errors.
- **Prevention Strategy:** The Jackfruit models are explicitly `float16`. Ensure the input image data type matches the required expected tensor types (often `np.float32`, even if quantized to `float16` under the hood by TFLite). Carefully inspect `interpreter.get_input_details()`.
- **Phase:** Addressed in ML Service model loading phase.

### 3. Asymmetric Image Resizing
- **Warning Sign:** Drastic accuracy drop in production versus validation datasets because mobile phones capture at 16:9 or 4:3, and the model expects 224x224 squares. 
- **Prevention Strategy:** If you skew/stretch the image to 224x224 instead of center-cropping or padding, the disease spots warp and confuse the models. Implement robust preprocessing padding/center-crop logic.
- **Phase:** Addressed in the Image Preprocessing phase of the ML pipeline.

### 4. Poor Field Connectivity
- **Warning Sign:** Farmers cannot upload 5MB high-resolution images from the field on Edge/3G networks.
- **Prevention Strategy:** The React Native app must compress the image locally (e.g., JPEG, 60% quality, max dimension 1024px) before uploading to S3, without destroying the visible symptoms.
- **Phase:** Addressed in the Mobile App Development phase.
