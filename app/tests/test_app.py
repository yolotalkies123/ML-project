import os
import sys
import pytest
from fastapi.testclient import TestClient

# Ensure the app module can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import app



# Initialize TestClient with your FastAPI app
client = TestClient(app)

# Sample test for the `/predict` endpoint
def test_predict():
    # Create a sample request payload
    payload = {"network_in": 100.0}
    
    # Send a POST request to the /predict endpoint
    response = client.post("/predict", json=payload)
    
    # Check if the response status code is 200 (OK)
    assert response.status_code == 200
    
    # Parse the JSON response
    data = response.json()
    
    # Check that the response contains the expected keys
    assert "polynomial_prediction" in data
    assert "decision_tree_prediction" in data
    
    # Optionally, you can add more specific checks on the predicted values
    # e.g., assert data['polynomial_prediction'] == expected_value

# Additional tests can be written for other scenarios, including edge cases
