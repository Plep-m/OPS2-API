from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello World !!!']

def test_connect_wrongpass_ko():
  response = client.post(
    "/connect/",
    headers={
      "Content-Type": "application/json"
    },
    json={
      "user_login": "sully_natsuya",
      "password": "notthepassword"
    }
  )
  assert response.status_code == 401
  assert response.json() == {"detail": "Invalid credentials"}
