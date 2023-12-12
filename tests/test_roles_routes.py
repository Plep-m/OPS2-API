from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_roles_ok():
    response = client.get("/roles/")
    assert response.status_code == 200

def test_post_role_ok():
    response = client.post(
        "/role/add",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "name": "test"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Role added successfully"}

def test_post_roles_ok():
    response = client.post(
        "/roles/add",
        headers={
            "Content-Type": "application/json"
        },
        json=["test1", "test2"]
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Roles added successfully"}

def test_update_role_ok():
    response = client.post(
        "/role/update?role_name=test&new_name=test3",
        headers={
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Role 'test' updated successfully to 'test3'"}

def test_delete_role_ok():
    response = client.post(
        "/role/delete?role_name=test3",
        headers={
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Role 'test3' deleted successfully"}