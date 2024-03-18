import requests
import json


payloads = {
    
}

def test_response(endpoint, payload, status_code):
    response = requests.put(endpoint, json=payload)
    assert response.status_code == status_code