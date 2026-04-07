# Roadmap

**3 phases** | **15 requirements mapped** | All v1 requirements covered ✓

| # | Phase | Goal | Requirements | Success Criteria |
|---|-------|------|--------------|------------------|
| 1 | ML Service Foundation | Build the FastAPI Python ML service with TFLite model loaders and SHAP explainability. | INFER-06, INFER-07, INFER-08, INFER-09 | 4 |
| 2 | Main Backend APIs | Develop the core Node/FastAPI user authentication, S3 integration, and dataset history routes. | AUTH-01, AUTH-02, INFER-04, INFER-05, CHAT-01, CHAT-02, CHAT-03, DATA-01 | 4 |
| 3 | Mobile Frontend App | Build the React Native/Expo app, integrate Camera APIs, display heatmaps, and implement historical logs. | INFER-01, INFER-02, INFER-03, DATA-02 | 3 |

## Phase Details

### Phase 1: ML Service Foundation
**Goal**: Build the FastAPI Python ML service with TFLite model loaders and SHAP explainability.
**UI hint**: no
**Requirements**: INFER-06, INFER-07, INFER-08, INFER-09
**Success criteria**:
1. S3 image download and preprocessing functions properly pad/crop 224x224 arrays.
2. TFLite inferences execute successfully without runtime errors (especially float16 models).
3. The Jackfruit logic router correctly directs Leaf/Fruit inputs.
4. SHAP heatmap PNGs are generated successfully under 10 seconds.

### Phase 2: Main Backend APIs
**Goal**: Develop the core FastAPI user authentication, S3 integration, and dataset history routes.
**UI hint**: no
**Requirements**: AUTH-01, AUTH-02, INFER-04, INFER-05, CHAT-01, CHAT-02, CHAT-03, DATA-01
**Success criteria**:
1. Users can register and obtain valid JWT tokens via `/login` endpoints.
2. The AI Chatbot accurately remembers the state of previously sent prediction contexts.
3. Prediction histories successfully save to MongoDB Atlas clusters.
4. Integrates seamlessly with the secondary ML Service endpoint.

### Phase 3: Mobile Frontend App
**Goal**: Build the React Native/Expo app, integrate Camera APIs, display heatmaps, and implement historical logs.
**UI hint**: yes
**Requirements**: INFER-01, INFER-02, INFER-03, DATA-02
**Success criteria**:
1. App successfully targets both Android and iOS natively via Expo framework.
2. Users can transition smoothly from Image Selection -> API Upload state spinners -> Result screens.
3. Heatmap images lazy load seamlessly from Amazon S3 bucket links on the prediction result UI.
