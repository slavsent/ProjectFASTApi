import json
import pytest
from starlette.testclient import TestClient
from fastapi import Depends
from sqlalchemy.orm import Session
from app import app
from core.db import get_db


@pytest.fixture(scope="module")
def result_holder():
    return []


def test_read_all_menus_null(db: Session = Depends(get_db)):
    client = TestClient(app)
    response = client.get("/api/v1/menus/")

    assert response.status_code == 200
    assert response.json() == []


def test_create_menu(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    test_payload = {"title": "menu 2", "description": "my super menu"}

    response = client.post("/api/v1/menus/", json=test_payload)
    data = response.json()['id']
    result_holder.append(data)
    assert response.status_code == 201
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["description"] == test_payload["description"]



def test_create_menu_invalid_json(db: Session = Depends(get_db)):
    client = TestClient(app)
    response = client.post("/api/v1/menus/", json={"title": "something"})
    assert response.status_code == 422


def test_read_menu(result_holder, db: Session = Depends(get_db)):
    test_data = {"title": "menu 2", "description": "my super menu"}
    client = TestClient(app)
    data = result_holder[0]
    response = client.get(f"/api/v1/menus/{data}")

    assert response.status_code == 200
    assert response.json()["title"] == test_data["title"]
    assert response.json()["description"] == test_data["description"]


def test_read_menu_incorrect_id(db: Session = Depends(get_db)):
    client = TestClient(app)
    response = client.get("/api/v1/menus/7855f909-3be6-4a45-84ed-c72941fe2419")
    assert response.status_code == 404
    assert response.json()["detail"] == "menu not found"


def test_read_all_menus(db: Session = Depends(get_db)):
    client = TestClient(app)
    response = client.get("/api/v1/menus/")

    assert response.status_code == 200
    assert response.json() != []


def test_update_menu(result_holder, db: Session = Depends(get_db)):
    test_update_data = {"title": "menu 2 update", "description": "my menu update"}

    client = TestClient(app)
    response = client.patch("/api/v1/menus/" + str(result_holder[0]), json=test_update_data)
    assert response.status_code == 200
    assert response.json()["title"] == test_update_data["title"]


def test_update_menu_invalid(db: Session = Depends(get_db)):
    test_update_data = {"title": "menu 2 update", "description": "my menu update"}
    client = TestClient(app)
    response = client.patch("/api/v1/menus/7855f909-3be6-4a45-84ed-c72941fe2419", json=test_update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == {'detail': 'menu not found'}


def test_remove_menu(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)

    response = client.delete("/api/v1/menus/" + str(result_holder[0]))
    assert response.status_code == 200
    assert response.json()["message"] == "The menu has been deleted"


def test_remove_menu_incorrect_id(db: Session = Depends(get_db)):
    client = TestClient(app)
    response = client.delete("/api/v1/menus/7855f909-3be6-4a45-84ed-c72941fe2419")
    assert response.status_code == 404
    assert response.json()["detail"] == 'menu not found'
