# Architecture Research: Agriculture Disease Detection App

## Component Boundaries
1. **Frontend App (React Native):** Handles UI, user state, camera interactions, and displays results/chat.
2. **Main Backend API (FastAPI):** Manages user authentication (JWT), MongoDB read/writes, and Redis caching. Relays ML requests to the ML Service.
3. **ML Service (FastAPI):** Dedicated bounded context running inference. Completely stateless. Loads TFLite models into memory at startup. Processes image bytes or S3 URLs, runs inference, runs SHAP, uploads heatmap to S3, returns JSON.

## Data Flow
Image Upload & Prediction:
1. Mobile app captures image and sends POST to Main Backend API.
2. API uploads raw image to S3, retrieves `image_url`.
3. API sends `image_url` and `crop_type` (Mango/Jackfruit) to ML Service.
4. ML Service downloads image, preprocesses, and passes through the correct TFLite pipeline.
5. ML Service generates SHAP explainer matrix, creates a visual heatmap, and uploads heatmap to S3.
6. ML Service returns Prediction, Confidence, Probabilities, and Heatmap URL.
7. Main API stores this result in MongoDB attached to the user.
8. Main API returns the aggregated object to the Mobile app.

Chatbot Flow:
1. User sends a message via Mobile App.
2. Mobile App sends message + `prediction_context_id` to Main API.
3. Main API pulls prediction context, injects into an LLM prompt (e.g., OpenAI/Gemini), and returns the tailored agronomy advice.
4. Main API logs chat history in MongoDB.

## Build Order Suggestions
1. Model scaffolding (ML Service) and TFLite verification.
2. Main backend and DB architecture configuration (Auth & Profiles).
3. Integration of ML Service to Main Backend.
4. Frontend Mobile App development (connecting UI to API).
5. Chatbot integration.
