from fastapi.testclient import TestClient
from main import app
import pytest

@pytest.fixture
def mock_open_file(mocker):
  return mocker.patch("builtins.open", mocker.mock_open())


client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ['Hello World !!!']

def test_get_users_ok():
  response = client.get("/users/")
  assert response.status_code == 200
  
def test_get_user_by_login_ok():
  response = client.get("/user/login/sully_natsuya")
  assert response.status_code == 200
  assert response.json()['firstname'] == "Sully"
  assert response.json()['lastname'] == "Natsuya"

def test_get_user_by_id_ok():
  response = client.get("/user/id/1")
  assert response.status_code == 200
  assert response.json()['firstname'] == "Sully"
  assert response.json()['lastname'] == "Natsuya"

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
  password = client.get("/user/login/sully_natsuya").json()['metas']['fpassword']
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
  password = client.get("/user/login/sully_natsuya").json()['metas']['fpassword']
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

def test_get_picture_for_user_ok():
  response = client.get("/users/sully_natsuya/profile_picture/")
  assert response.status_code == 200
  assert response.headers['Content-Type'] == "image/png"

def test_get_picture_for_user_official_ok():
  response = client.get("/users/sully_natsuya/profile_picture/official/")
  assert response.status_code == 200
  assert response.headers['Content-Type'] == "image/png"

def test_get_picture_for_user_ko():
  response = client.get("/users/sully_nsuya/profile_picture")
  assert response.status_code == 200
  assert response.json() == {"message": "User not found"}

def test_get_picture_for_user_ko_2():
  response = client.get("/users/nagisa_shiota/profile_picture/official")
  assert response.status_code == 200
  assert response.json() == {"message": "Invalid gender"}

def test_upload_pickture_ko():
  response = client.post(
    "/users/sully_nuya/upload_profile_picture/",
    headers={
      "Content-Type": "multipart/form-data"
    },
    files=[
      ('file', 'test.jpg', 'image/jpeg')
    ]
  )
  assert response.status_code == 200
  assert response.json() == {"message": "User not found"}
