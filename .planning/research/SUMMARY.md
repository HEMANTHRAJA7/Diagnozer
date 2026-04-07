# Summary Research: Agriculture Disease Detection App

## Synthesis of Key Findings

1. **Stack Consistency:** The user-defined stack (React Native + FastAPI + TFLite + MongoDB/Redis/S3) is an industry-standard, robust approach. Relying on Google Cloud Run correctly prevents idle GPU/CPU billing for the stateless ML service.
2. **SHAP Integration:** Transitioning from Grad-CAM to SHAP is a massive leap in explainability quality, but introduces the biggest architectural risk: computation latency. The ML Service must carefully handle SHAP explainer instantiation and generation to avoid blocking requests or timing out Cloud Run responses.
3. **Pipeline Complexity:** The Jackfruit pipeline requires chained orchestration. `StageA` must execute fast to determine whether the image is "Fruit" or "Leaf", then immediately feed the original image tensor into either `StageB_Fruit` or `StageB_Leaf`. This routing must be fault-tolerant (e.g., if StageA predicts "Leaf" with only 51% confidence).
4. **Field Environment Reality:** We must guarantee that the mobile frontend performs aggressive but symptom-preserving image compression before the upload sequence starts to account for terrible agricultural field network bandwidth.

## Conclusion
The project is structurally sound. The immediate focus must be creating airtight Python APIs that wrap the 4 `.tflite` models perfectly, utilizing correct input tensor resizing strategies and establishing an efficient SHAP matrix generation approach. Once the ML Service succeeds, orchestrating the backend and frontend becomes a straightforward data integration task.
