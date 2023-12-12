from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_get_roles_ok():
    response = client.get("/tags/")
    assert response.status_code == 200

def test_post_role_ok():
    response = client.post(
        "/tag/add",
        headers={
            "Content-Type": "application/json"
        },
        json={
            "name": "test"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Tag added successfully"}

def test_post_tags_ok():
    response = client.post(
        "/tags/add",
        headers={
            "Content-Type": "application/json"
        },
        json=["test1", "test2"]
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Tags added successfully"}

def test_update_tag_ok():
    response = client.post(
        "/tag/update?tag_name=test&new_name=test3",
        headers={
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Tag 'test' updated successfully to 'test3'"}

def test_delete_tag_ok():
    response = client.post(
        "/tag/delete?tag_name=test3",
        headers={
            "Content-Type": "application/json"
        }
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Tag 'test3' deleted successfully"}