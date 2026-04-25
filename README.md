# 🌿 Diagnozer

**AI-Powered Agriculture Disease Detection with Explainable AI**

Diagnozer is a full-stack mobile application that helps farmers and agronomists detect diseases in **Mango** and **Jackfruit** crops using deep learning. Users capture or upload images of leaves and fruits, receive instant disease predictions with confidence scores, and get **SHAP-based explainability heatmaps** highlighting exactly which regions of the image influenced the diagnosis. A built-in **Gemini-powered chatbot** provides actionable treatment and prevention advice.

---

## 📋 Table of Contents

- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Disease Classes](#-disease-classes)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Setup & Installation](#-setup--installation)
- [Running Locally](#-running-locally)
- [API Reference](#-api-reference)
- [Deployment](#-deployment)
- [Environment Variables](#-environment-variables)
- [License](#-license)

---

## 🏗 Architecture

```
┌─────────────────────┐
│   React Native App  │
│     (Expo SDK 54)   │
└────────┬────────────┘
         │  REST API
         ▼
┌─────────────────────┐       ┌─────────────────────┐
│   Main Backend      │──────▶│   ML Service         │
│   (FastAPI :8001)   │ proxy │   (FastAPI :8000)     │
│                     │       │                       │
│ • JWT Auth          │       │ • TFLite Inference    │
│ • MongoDB Atlas     │       │ • SHAP Explainability │
│ • Gemini Chatbot    │       │ • Heatmap Generation  │
│ • S3 Integration    │       │ • S3 Upload           │
└─────────────────────┘       └───────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────────┐       ┌───────────────────────┐
│   MongoDB Atlas     │       │   Amazon S3           │
│   (User data,       │       │   (Images, Heatmaps)  │
│    chat history,    │       │                       │
│    predictions)     │       │                       │
└─────────────────────┘       └───────────────────────┘
```

**Inference Pipeline:**

```
User Image → S3 Upload → Preprocessing → TFLite Model Inference → SHAP Heatmap → JSON Response
```

The **Jackfruit pipeline** uses a two-stage classification approach:
1. **Stage A** — Classifies the image as either **Fruit** or **Leaf**
2. **Stage B** — Routes to the appropriate disease detection model based on Stage A's output

---

## 🛠 Tech Stack

| Layer            | Technology                                                     |
| ---------------- | -------------------------------------------------------------- |
| **Mobile App**   | React Native, Expo SDK 54, React Navigation 7                  |
| **Main Backend** | Python 3.10, FastAPI, Motor (async MongoDB), python-jose (JWT)  |
| **ML Service**   | Python 3.10, FastAPI, TensorFlow Lite, SHAP, scikit-image       |
| **Database**     | MongoDB Atlas                                                   |
| **Storage**      | Amazon S3                                                       |
| **AI Chatbot**   | Google Gemini (via `google-genai`)                               |
| **Deployment**   | Docker, Google Cloud Run                                        |

---

## 🔬 Disease Classes

### Mango (single-stage model)

| Index | Class            |
| ----- | ---------------- |
| 0     | Anthracnose      |
| 1     | Bacterial Canker |
| 2     | Healthy          |
| 3     | Scab             |
| 4     | Stem End Rot     |

**Input size:** 240 × 240 &nbsp;|&nbsp; **Model:** `mango_dynamic_range.tflite`

### Jackfruit (two-stage pipeline)

**Stage A — Fruit vs. Leaf** (`StageA_Fruit_vs_Leaf_float16.tflite`)

| Index | Class |
| ----- | ----- |
| 0     | Fruit |
| 1     | Leaf  |

**Stage B — Fruit Diseases** (`StageB_Fruit_float16.tflite`)

| Index | Class             |
| ----- | ----------------- |
| 0     | Fruit Damage      |
| 1     | Healthy Jackfruit |
| 2     | Rhizopus Rot      |

**Stage B — Leaf Diseases** (`StageB_Leaf_float16.tflite`)

| Index | Class       |
| ----- | ----------- |
| 0     | Healthy Leaf|
| 1     | Leaf Blight |
| 2     | Leaf Spot   |

**Input size:** 300 × 300

---

## 📁 Project Structure

```
Diagnozer/
├── diagnozer-app/              # React Native mobile app (Expo)
│   ├── App.js                  # Root navigator
│   ├── src/
│   │   ├── screens/
│   │   │   ├── LoginScreen.js
│   │   │   ├── HomeScreen.js
│   │   │   ├── ScannerScreen.js
│   │   │   ├── ResultScreen.js
│   │   │   └── ChatScreen.js
│   │   ├── services/           # API client utilities
│   │   └── theme/              # App theming & styles
│   ├── app.json
│   └── package.json
│
├── main-backend/               # Primary API gateway (FastAPI)
│   ├── app/
│   │   ├── main.py             # App entrypoint
│   │   ├── api/routes/
│   │   │   ├── auth.py         # Register / Login (JWT)
│   │   │   ├── inference.py    # Proxy to ML Service
│   │   │   └── chat.py         # Gemini chatbot
│   │   ├── core/config.py      # Settings & env vars
│   │   ├── db/                 # MongoDB connection
│   │   └── models/             # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
│
├── ml-service/                 # ML inference microservice (FastAPI)
│   ├── app/
│   │   ├── main.py             # App entrypoint
│   │   ├── api/routes/         # /predict/mango, /predict/jackfruit
│   │   ├── ml/
│   │   │   ├── mango_model.py      # Mango predictor singleton
│   │   │   ├── jackfruit_model.py  # Jackfruit two-stage predictor
│   │   │   ├── shap_explainer.py   # SHAP heatmap generator
│   │   │   └── tflite_utils.py     # TFLite model wrapper
│   │   ├── core/config.py
│   │   ├── schemas/
│   │   └── services/
│   ├── models/                 # Pre-trained TFLite model files
│   │   ├── mango_dynamic_range.tflite
│   │   ├── StageA_Fruit_vs_Leaf_float16.tflite
│   │   ├── StageB_Fruit_float16.tflite
│   │   ├── StageB_Leaf_float16.tflite
│   │   └── class_names_*.json
│   ├── Dockerfile
│   └── requirements.txt
│
├── .gitignore
└── README.md
```

---

## ✅ Prerequisites

- **Python** 3.10+
- **Node.js** 18+ & **npm**
- **Expo CLI** — `npm install -g expo-cli`
- **MongoDB** (local instance or Atlas connection string)
- **AWS credentials** (for S3 uploads; optional — local mock mode available)
- **Google Gemini API key** (for the chatbot)

---

## ⚙ Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/HEMANTHRAJA7/Diagnozer.git
cd Diagnozer
```

### 2. ML Service

```bash
cd ml-service
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

pip install -r requirements.txt
```

Create a `.env` file in `ml-service/`:

```env
MOCK_S3_UPLOAD=true
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
S3_BUCKET_NAME=your_bucket_name
```

### 3. Main Backend

```bash
cd main-backend
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt
```

Create a `.env` file in `main-backend/`:

```env
MONGODB_URL=mongodb+srv://<user>:<pass>@cluster.mongodb.net
DB_NAME=diagnozer_db
SECRET_KEY=your_jwt_secret_key
ML_SERVICE_URL=http://localhost:8000
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Mobile App

```bash
cd diagnozer-app
npm install
```

---

## 🚀 Running Locally

Start each service in a **separate terminal**:

```bash
# Terminal 1 — ML Service (port 8000)
cd ml-service
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000

# Terminal 2 — Main Backend (port 8001)
cd main-backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8001

# Terminal 3 — Mobile App
cd diagnozer-app
npm start
```

> **Tip:** Use the Expo Go app on your phone to scan the QR code and run the app on a physical device.

### Quick Test — Register a User

```bash
curl -X POST http://localhost:8001/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email": "test@diagnozer.com", "password": "test123", "full_name": "Test User"}'
```

---

## 📡 API Reference

### Main Backend (`localhost:8001`)

| Method | Endpoint                    | Description                       |
| ------ | --------------------------- | --------------------------------- |
| GET    | `/api/v1/health`            | Health check                      |
| POST   | `/api/v1/auth/register`     | Register a new user               |
| POST   | `/api/v1/auth/login`        | Login and receive JWT token       |
| POST   | `/api/v1/inference/predict` | Upload image & get prediction     |
| POST   | `/api/v1/chat/message`      | Send message to AI chatbot        |
| GET    | `/api/v1/chat/history`      | Retrieve chat history             |

### ML Service (`localhost:8000`)

| Method | Endpoint                     | Description                            |
| ------ | ---------------------------- | -------------------------------------- |
| GET    | `/api/v1/health`             | Health check                           |
| POST   | `/api/v1/predict/mango`      | Classify mango disease + SHAP heatmap  |
| POST   | `/api/v1/predict/jackfruit`  | Classify jackfruit disease + SHAP heatmap |

---

## 🐳 Deployment

Both backend services are containerized and configured for **Google Cloud Run**.

### Build & Deploy with Docker

```bash
# ML Service
cd ml-service
docker build -t diagnozer-ml-service .
docker run -p 8000:8000 --env-file .env diagnozer-ml-service

# Main Backend
cd main-backend
docker build -t diagnozer-main-backend .
docker run -p 8001:8001 --env-file .env diagnozer-main-backend
```

### Deploy to Google Cloud Run

```bash
# ML Service
gcloud run deploy diagnozer-ml-service \
  --source ./ml-service \
  --region us-central1 \
  --allow-unauthenticated

# Main Backend
gcloud run deploy diagnozer-main-backend \
  --source ./main-backend \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🔐 Environment Variables

### ML Service

| Variable               | Description                        | Default         |
| ---------------------- | ---------------------------------- | --------------- |
| `AWS_ACCESS_KEY_ID`    | AWS access key for S3              | —               |
| `AWS_SECRET_ACCESS_KEY`| AWS secret key for S3              | —               |
| `S3_BUCKET_NAME`       | S3 bucket for images & heatmaps   | —               |
| `AWS_REGION`           | AWS region                         | `us-east-1`     |
| `MOCK_S3_UPLOAD`       | Save locally instead of S3         | `true`          |

### Main Backend

| Variable                     | Description                       | Default                      |
| ---------------------------- | --------------------------------- | ---------------------------- |
| `MONGODB_URL`                | MongoDB connection string         | `mongodb://localhost:27017`  |
| `DB_NAME`                    | Database name                     | `diagnozer_db`               |
| `SECRET_KEY`                 | JWT signing secret                | dev key (change in prod!)    |
| `ACCESS_TOKEN_EXPIRE_MINUTES`| Token expiry in minutes           | `43200` (30 days)            |
| `ML_SERVICE_URL`             | URL of the ML microservice        | `http://localhost:8000`      |
| `GEMINI_API_KEY`             | Google Gemini API key for chatbot | —                            |

---

## 📄 License

This project is developed as an academic/research project.

---

<p align="center">
  Built with ❤️ using FastAPI, TensorFlow Lite, SHAP & React Native
</p>

