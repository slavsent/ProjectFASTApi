from core.db import get_db
from app import app
from sqlalchemy.orm import Session
from fastapi import Depends
from starlette.testclient import TestClient
import pytest
import json

import os

os.environ['TESTING'] = 'True'


@pytest.fixture(scope="module")
def result_holder():
    return []


@pytest.fixture(scope="module")
def result_holder_submenu():
    return []


def test_create_menu(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    test_payload = {"title": "menu 2", "description": "my super menu"}

    response = client.post("/api/v1/menus/", json=test_payload)
    data = response.json()['id']
    result_holder.append(data)
    assert response.status_code == 201
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["description"] == test_payload["description"]


def test_read_all_submenus_null(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    data = result_holder[0]
    response = client.get("/api/v1/menus/"+str(data)+"/submenus/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    test_payload = {"title": "submenu 1", "description": "my submenu"}
    data_menu = result_holder[0]
    response = client.post(
        f"/api/v1/menus/{data_menu}/submenus/", json=test_payload,
    )
    data = response.json()['id']
    result_holder_submenu.append(data)

    assert response.status_code == 201
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["description"] == test_payload["description"]


def test_create_submenu_invalid_json(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    response = client.post(
        f"/api/v1/menus/{data_menu}/submenus/", json={"title": "something"},
    )

    assert response.status_code == 422


def test_read_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    test_data = {"title": "submenu 1", "description": "my submenu"}
    client = TestClient(app)
    data_menu = result_holder[0]
    data = result_holder_submenu[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/{data}")

    assert response.status_code == 200
    assert response.json()["title"] == test_data["title"]
    assert response.json()["description"] == test_data["description"]


def test_read_submenu_incorrect_id(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    response = client.get(
        f"/api/v1/menus/{data_menu}/submenus/7855f909-3be6-4a45-84ed-c72941fe2419",
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


def test_read_all_submenus(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/")

    assert response.status_code == 200
    assert response.json() != []


def test_update_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    test_update_data = {
        "title": "submenu 2 update",
        "description": "my submenu update",
    }

    client = TestClient(app)
    data_menu = result_holder[0]
    data = result_holder_submenu[0]
    response = client.patch(
        f"/api/v1/menus/{data_menu}/submenus/{data}", json=test_update_data,
    )

    assert response.status_code == 200
    assert response.json()["title"] == test_update_data["title"]


def test_update_submenu_invalid(result_holder, db: Session = Depends(get_db)):
    test_update_data = {
        "title": "submenu 2 update",
        "description": "my submenu update",
    }
    client = TestClient(app)
    data_menu = result_holder[0]
    response = client.patch(
        f"/api/v1/menus/{data_menu}/submenus/7855f909-3be6-4a45-84ed-c72941fe2419", json=test_update_data,
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "submenu not found"


def test_remove_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data = result_holder_submenu[0]
    response = client.delete(f"/api/v1/menus/{data_menu}/submenus/{data}")
    assert response.status_code == 200
    assert response.json()["message"] == "The submenu has been deleted"


def test_remove_submenu_incorrect_id(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    response = client.delete(
        f"/api/v1/menus/{data_menu}/submenus/7855f909-3be6-4a45-84ed-c72941fe2419",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == 'submenu not found'


def test_remove_menu(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)

    response = client.delete("/api/v1/menus/" + str(result_holder[0]))
    assert response.status_code == 200
    assert response.json()["message"] == "The menu has been deleted"
