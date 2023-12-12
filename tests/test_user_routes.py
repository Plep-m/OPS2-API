import pytest
import os
from fastapi import UploadFile
from fastapi.testclient import TestClient
from main import app
from models.user_model import User
from src.database import SessionLocal
from routes.users_routes import get_db, oauth2_scheme, get_picture_path
from jwt import PyJWTError

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

def test_post_picture_for_user_ko():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natya/upload_profile_picture/',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "User not found"}

def test_post_picture_for_user_ok_1():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natsuya/upload_profile_picture/',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "Profile picture uploaded successfully"}

def test_post_picture_for_user_ok_2():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natsuya/upload_profile_picture/',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "Profile picture uploaded successfully"}

def test_post_picture_for_user_official_ko():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natya/upload_profile_picture/official',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "User not found"}

def test_post_picture_for_user_official_ok_1():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natsuya/upload_profile_picture/official',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "Profile picture uploaded successfully"}

def test_post_picture_for_user_official_ok_2():
  with open('resources/basics/man.png', 'rb') as file:
    upload_file = UploadFile(file=file, filename='man.png')
            
    response = client.post(
                f'/users/sully_natsuya/upload_profile_picture/official',
                files={'file': ('man.png', file, 'image/image/png')},
              )
    assert response.status_code == 200
    assert response.json() == {"message": "Profile picture uploaded successfully"}

def test_create_user():
  user_data = {
      "firstname": "John",
      "lastname": "Doe",
      "gender": "male",
      "phone": "+33612345678",
      "postal_code": "45422",
      "address": "1 rue de la Paix",
      "city": "Paris",
      "country": "France",
      "roles": [{"name": "administrator"}]
  }

  response = client.post(
      "/users/",
      json=user_data,
      headers={
          "Content-Type": "application/json"
      },
  )

  assert response.status_code == 200
  assert response.json() == {"message": "User created successfully"}

  with SessionLocal() as db:
      created_user = db.query(User).filter_by(firstname="John").first()
      assert created_user is not None
      assert created_user.lastname == "Doe"

def test_get_current_user_user_login_none(mocker):
    mocker.patch("routes.users_routes.jwt.decode", return_value={"sub": None})
    mocker.patch("routes.users_routes.get_db", return_value=mocker.Mock(query=mocker.Mock(
        filter=mocker.Mock(return_value=mocker.Mock(first=mocker.Mock(return_value=None)))
    )))

    response = client.get(
            "/verify-token/",
            headers={"Authorization": "Bearer valid_token"},
        )
        
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_get_current_user_ko_user_none(mocker):
    mocker.patch("routes.users_routes.jwt.decode", return_value={"sub": "user_login"})
    mocker.patch("routes.users_routes.get_db", return_value=mocker.Mock(query=mocker.Mock(
        filter=mocker.Mock(return_value=mocker.Mock(first=mocker.Mock(return_value=None)))
    )))

    response = client.get(
            "/verify-token/",
            headers={"Authorization": "Bearer valid_token"},
        )
        
    assert response.status_code == 401
    assert response.json() == {"detail": "Could not validate credentials"}

def test_get_picture_path_exists(mocker):
    mocker.patch("os.path.exists", return_value=True)

    # Define user_login and extensions for the test
    user_login = "test_user"
    extensions = ["jpg", "png", "gif"]
    big_extension = "_big"

    # Call the function
    result = get_picture_path(user_login, extensions, big_extension)
    os.path.exists.assert_called_once_with(f"resources/user/profile_picture/{user_login}/{user_login}_big.jpg")
    expected_path = f"resources/user/profile_picture/{user_login}/{user_login}_big.jpg"
    
    assert result == expected_path