from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello World !!!']

def test_verify_token_ko():
    response = client.get("/verify-token/")
    assert response.status_code == 401
    assert response.json() == {'detail': 'Could not validate credentials'}