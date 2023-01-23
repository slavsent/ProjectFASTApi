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


@pytest.fixture(scope="module")
def result_holder_submenu():
    return []


@pytest.fixture(scope="module")
def result_holder_dish():
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


def test_create_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    test_payload = {"title": "submenu 1", "description": "my submenu"}
    data_menu = result_holder[0]
    response = client.post(f"/api/v1/menus/{data_menu}/submenus/", json=test_payload)
    data = response.json()['id']
    result_holder_submenu.append(data)

    assert response.status_code == 201
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["description"] == test_payload["description"]


def test_read_all_dish_null(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_dish(result_holder, result_holder_submenu, result_holder_dish, db: Session = Depends(get_db)):
    client = TestClient(app)
    test_payload = {"title": "dish 1", "description": "soup", "price": "12.50"}
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.post(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/", json=test_payload)
    data = response.json()['id']
    result_holder_dish.append(data)

    assert response.status_code == 201
    assert response.json()["title"] == test_payload["title"]
    assert response.json()["description"] == test_payload["description"]
    assert response.json()["price"] == test_payload["price"]


def test_create_dish_invalid_json(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.post(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/", json={"title": "something"})

    assert response.status_code == 422


def test_read_dish(result_holder, result_holder_submenu, result_holder_dish, db: Session = Depends(get_db)):
    test_data = {"title": "dish 1", "description": "soup", "price": "12.50"}
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    data = result_holder_dish[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/{data}")

    assert response.status_code == 200
    assert response.json()["title"] == test_data["title"]
    assert response.json()["description"] == test_data["description"]
    assert response.json()["price"] == test_data["price"]


def test_read_dish_incorrect_id(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/7855f909-3be6-4a45-84ed-c72941fe2419")

    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


def test_read_all_dish(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.get(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/")

    assert response.status_code == 200
    assert response.json() != {}


def test_update_dish(result_holder, result_holder_submenu, result_holder_dish, db: Session = Depends(get_db)):
    test_update_data = {"title": "dish 2 update", "description": "my soup update", "price": "14.50"}

    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    data = result_holder_dish[0]
    response = client.patch(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/{data}", json=test_update_data)

    assert response.status_code == 200
    assert response.json()["title"] == test_update_data["title"]


def test_update_dish_invalid(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    test_update_data = {"title": "dish 2 update", "description": "my soup update", "price": "14.50"}
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.patch(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/7855f909-3be6-4a45-84ed-c72941fe2419", json=test_update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "dish not found"


def test_remove_dish(result_holder, result_holder_submenu, result_holder_dish, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    data = result_holder_dish[0]
    response = client.delete(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/{data}")
    assert response.status_code == 200
    assert response.json()["message"] == "The dish has been deleted"


def test_remove_dish_incorrect_id(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data_submenu = result_holder_submenu[0]
    response = client.delete(f"/api/v1/menus/{data_menu}/submenus/{data_submenu}/dishes/7855f909-3be6-4a45-84ed-c72941fe2419")
    assert response.status_code == 404
    assert response.json()["detail"] == 'dish not found'


def test_remove_submenu(result_holder, result_holder_submenu, db: Session = Depends(get_db)):
    client = TestClient(app)
    data_menu = result_holder[0]
    data = result_holder_submenu[0]
    response = client.delete(f"/api/v1/menus/{data_menu}/submenus/{data}")
    assert response.status_code == 200
    assert response.json()["message"] == "The submenu has been deleted"


def test_remove_menu(result_holder, db: Session = Depends(get_db)):
    client = TestClient(app)

    response = client.delete("/api/v1/menus/" + str(result_holder[0]))
    assert response.status_code == 200
    assert response.json()["message"] == "The menu has been deleted"