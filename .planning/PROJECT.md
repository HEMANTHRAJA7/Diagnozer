# Diagnozer

## What This Is

Diagnozer is an AI-powered agriculture disease detection mobile app. It allows users to upload or capture images of Mango or Jackfruit leaves/fruits to receive disease predictions, confidence scores, and SHAP-based explainable AI heatmaps, while providing a conversational chatbot for treatment and prevention advice.

## Core Value

Provide accurate, explainable agriculture disease detection and actionable treatment advice for Mango and Jackfruit crops using pre-trained TensorFlow Lite models.

## Requirements

### Validated

(None yet — ship to validate)

### Active

- [ ] Mobile app with auth (sign up / log in).
- [ ] Image capture and upload functionality for Mango and Jackfruit.
- [ ] Cloud-hosted ML APIs (FastAPI) that process images through pre-trained TFLite models.
- [ ] Mango specific pipeline using `mango_dynamic_range.tflite`.
- [ ] Jackfruit specific pipeline using `StageA_Fruit_vs_Leaf_float16.tflite` followed by StageB leaf or fruit models.
- [ ] SHAP integration to generate explainable AI heatmaps.
- [ ] Generative AI chatbot to answer questions about treatment, prevention, severity, and irrigation.
- [ ] Persistent storage of prediction history and chatbot history in MongoDB.

### Out of Scope

- [Training new ML models] — Pre-trained models are provided and must be used as-is.
- [Support for crops other than Mango and Jackfruit] — Scope restricted to provided models.

## Context

- **Workflow**: 
  - User uploads image -> S3 -> ML Service -> Preprocessing -> TFLite Inference -> SHAP Heatmap -> JSON Response.
- **Models Used**: 
  - `mango_dynamic_range.tflite`
  - `StageA_Fruit_vs_Leaf_float16.tflite`
  - `StageB_Fruit_float16.tflite`
  - `StageB_Leaf_float16.tflite`

## Constraints

- **Tech Stack**: Frontend must use React Native, Expo, React Navigation.
- **Backend**: FastAPI, JWT, MongoDB Atlas, Redis.
- **ML Service**: FastAPI, TensorFlow Lite, SHAP.
- **Storage**: Amazon S3 for images and heatmaps.
- **Deployment**: Docker, Google Cloud Run, Render.

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use SHAP for Explainability | User request to use SHAP instead of Grad-CAM for more robust feature attribution. | — Pending |

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-03-31 after initialization*
