from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello World !!!']

def test_verify_token_ok():
    client.post("/connect/", data={"user_login": "sully_natsuya", "password": "admin"})
    response = client.get("/verify-token/")
    assert response.status_code == 200
    assert response.json() == {"login": "admin"}