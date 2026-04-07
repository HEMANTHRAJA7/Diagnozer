# Stack Research: Agriculture Disease Detection App

## Executive Summary
The selected stack (React Native + FastAPI + TFLite + SHAP) is optimal for an AI-powered agriculture mobile app requiring explainability. It balances mobile accessibility with high-performance python-based ML processing. Google Cloud Run ensures auto-scaling for inference spikes without persistent server costs.

## Components

### Frontend (Mobile)
- **Framework:** React Native with Expo
- **Rationale:** Cross-platform (iOS/Android) code reuse, fast development cycle, excellent camera API support for image capture.
- **Key Libraries:** `expo-camera`, `expo-image-picker`, `axios`, `react-navigation`.

### Backend (API & DB)
- **Framework:** FastAPI (Python)
- **Rationale:** Python is mandatory for ML/SHAP integration. FastAPI provides high concurrency and auto-generated OpenAPI docs.
- **Database:** MongoDB Atlas (NoSQL) for flexible schema storage of chatbot history and prediction results. Redis for session caching and rate limiting.

### ML Service
- **Inference Server:** FastAPI
- **Model Runtime:** TensorFlow Lite (`tflite-runtime`)
- **Rationale:** TFLite models are fast, lightweight, and pre-trained.
- **Explainability:** SHAP
- **Rationale:** SHAP provides mathematically robust feature attribution, explaining exactly which pixels influenced the disease prediction (more comprehensive than Grad-CAM).

### Infrastructure
- **Storage:** Amazon S3 (for storing raw uploaded images and generated SHAP heatmaps).
- **Deployment:** Docker + Google Cloud Run (for the ML Service and Backend) ensures stateless horizontal scaling. Render can be utilized for secondary fallback hosting.

## What NOT To Use
- **Heavy CNNs via PyTorch in Production**: Stick to the pre-provided TFLite models to avoid massive memory overhead on Cloud Run.
- **Grad-CAM**: Explicitly avoided per user request; use SHAP instead.
