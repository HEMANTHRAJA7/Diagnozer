# Features Research: Agriculture Disease Detection App

## Table Stakes (Must Have)
These are mandatory features without which users will reject the app:
- **Authentication:** Secure Sign up / Log in flow via JWT.
- **Image Capture:** In-app camera and gallery upload.
- **Disease Inference:** Real-time prediction (using Mango and Jackfruit TFLite models).
- **Result Visualization:** Display predicted disease and confidence score.
- **History Logs:** Save past predictions to the user's profile for later reference.

## Differentiators (Competitive Advantage)
- **SHAP Explainability Heatmap:** Showing the user exactly *why* the AI made the prediction builds massive trust, especially for farmers and agronomists.
- **Multi-Stage Pipeline (Jackfruit):** Smart dynamic routing between a Fruit vs Leaf model, and then specific leaf/fruit classification models.
- **Generative AI Chatbot:** Context-aware assistant that knows the predicted disease and can answer targeted questions regarding treatments, fertilizers, and irrigation.

## Anti-Features (Do Not Build)
- **On-device Inference:** Although TFLite suggests on-device usage, the requirement dictates "Cloud-hosted ML APIs." Doing on-device inference would bloat the app size and make updating models difficult. Avoid deploying models to the mobile app bundle directly.
- **Generic Chatbot:** A generic chatbot that doesn't understand the user's currently predicted disease will cause frustration. The chat must be context-aware.
