import sys
import os

# Add the parent directory to sys.path so Python can find your app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    # Adjust the expected response as needed
    assert response.json() == {"message": "FastAPI Patient API is running."}