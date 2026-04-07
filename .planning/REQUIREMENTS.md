# Requirements

## v1 Requirements

### Authentication
- [ ] **AUTH-01**: User can sign up with email/password.
- [ ] **AUTH-02**: User can log in and securely maintain a session using JWT.

### Core Inference
- [ ] **INFER-01**: User can capture an image via mobile camera.
- [ ] **INFER-02**: User can select an image from the mobile phone gallery.
- [ ] **INFER-03**: User must select the crop type (Mango or Jackfruit) prior to inference.
- [ ] **INFER-04**: App securely uploads the selected image to Amazon S3.
- [ ] **INFER-05**: App securely invokes ML Service with the S3 image link.
- [ ] **INFER-06**: ML Service classifies Mango images using `mango_dynamic_range.tflite`.
- [ ] **INFER-07**: ML Service classes Jackfruit images using a two-stage pipeline.
- [ ] **INFER-08**: ML Service calculates and generates a SHAP feature attribution heatmap.
- [ ] **INFER-09**: ML Service uploads the SHAP heatmap to S3 and returns the heatmap URL.

### Chatbot
- [ ] **CHAT-01**: User can ask a generative AI chatbot for disease treatment advice.
- [ ] **CHAT-02**: Chatbot incorporates the latest ML prediction context (disease severity, type).
- [ ] **CHAT-03**: Chat history is persisted and loadable per user via MongoDB.

### Data & History
- [ ] **DATA-01**: System saves all inference results (disease, confidence scores, probabilities, heatmap URL) to the user's MongoDB profile.
- [ ] **DATA-02**: User can view a historical log of their past disease predictions.

## v2 Requirements
- Support for offline inference if internet is unavailable.
- Multi-language support for the chatbot interface.

## Out of Scope
- **Training Custom Models**: The provided TensorFlow Lite models must be used. No new models will be trained.
- **Grad-CAM**: The user explicitly requested SHAP over Grad-CAM.
- **Support for non-Mango/Jackfruit Crops**: Scope is rigidly locked to the provided models.

## Traceability
<!-- Updated by roadmap generation -->
