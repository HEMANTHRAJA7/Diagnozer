# Diagnozer AI Assistant Context

This project uses the Get Shit Done (GSD) workflow system.

1. **Check State**: Always read `.planning/STATE.md` to understand current context.
2. **Execute Phases**: We work phase by phase according to `.planning/ROADMAP.md`.
3. **Use Artifacts**: Maintain all planning context in `.planning/`.
4. Do not delete or compress files without explicit user command.

The tech stack relies heavily on TensorFlow Lite and SHAP explainability inside a stateless FastAPI microservice hosted on Google Cloud Run.
