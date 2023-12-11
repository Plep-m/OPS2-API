from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello World !!!']

def test_get_users_ok():
  response = client.get("/users/")
  assert response.status_code == 200
  
def test_get_user_by_login_ok():
  response = client.get("/user/sully_natsuya")
  assert response.status_code == 200

def test_get_user_by_id_ok():
  response = client.get("/user/1")
  assert response.status_code == 200

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

def test_connect_ok():
  password = client.get("/user/sully_natsuya").json()['metas']['fpassword']
  response = client.post(
    "/connect/",
    headers={
      "Content-Type": "application/json"
    },
    json={
      "user_login": "sully_natsuya",
      "password": password
    }
  )
  assert response.status_code == 200

def test_verify_token_ok():
  password = client.get("/user/sully_natsuya").json()['metas']['fpassword']
  token = client.post(
    "/connect/",
    headers={
      "Content-Type": "application/json"
    },
    json={
      "user_login": "sully_natsuya",
      "password": password
    }
  ).json()['access_token']
  response = client.get(
    "/verify-token/",
    headers={
      "Authorization": f"Bearer {token}"
    }
  )
  assert response.status_code == 200
  assert response.json() == {"login": "sully_natsuya"}

def test_verify_token_ko():
  response = client.get(
    "/verify-token/",
    headers={
      "Authorization": f"Bearer notatoken"
    }
  )
  assert response.status_code == 401
  assert response.json() == {"detail": "Could not validate credentials"}