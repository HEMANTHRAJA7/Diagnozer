import os
import io
from fastapi.testclient import TestClient
from PIL import Image

# Change working directory so models load correctly relative to the project root
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app.main import app

client = TestClient(app)

print("\n--- DIAGNOZER SERVER TEST ---")

# 1. Test Health Route
print("\n1. Testing GET /api/v1/health")
health_resp = client.get("/api/v1/health")
print(f"Status: {health_resp.status_code} - Body: {health_resp.json()}")

# 2. Test Mango Inference Pipeline
print("\n2. Testing POST /api/v1/predict/mango")
# Generate a dummy RGB image (just to pass through the preprocessing/inference safely)
dummy_img = Image.new('RGB', (500, 500), color=(120, 180, 80))
buf = io.BytesIO()
dummy_img.save(buf, format='JPEG')
buf.seek(0)

mango_resp = client.post(
    "/api/v1/predict/mango",
    files={"file": ("dummy_mango.jpg", buf, "image/jpeg")}
)
print(f"Status: {mango_resp.status_code}")
if mango_resp.status_code == 200:
    print(f"Success! Body: {mango_resp.json()}")
else:
    print(f"Error Body: {mango_resp.text}")

print("\n--- END OF TESTS ---\n")
