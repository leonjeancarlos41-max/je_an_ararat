# tests/test_endpoints.py
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.models.data import store

client = TestClient(app)

def test_list_users_initial():
    res = client.get("/api/users")
    assert res.status_code == 200
    assert isinstance(res.json(), list)

def test_create_user_and_get():
    payload = {"name": "Test User", "email": "test@example.com"}
    res = client.post("/api/users", json=payload)
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == payload["name"]
    uid = data["id"]

    # get by id
    res2 = client.get(f"/api/users/{uid}")
    assert res2.status_code == 200
    assert res2.json()["email"] == payload["email"]

def test_create_task_and_update_delete():
    # create user to link
    res_u = client.post("/api/users", json={"name":"Owner","email":"owner@example.com"})
    uid = res_u.json()["id"]

    # create task
    res = client.post("/api/tasks", json={"title":"Tarea test", "description":"desc", "owner_id": uid})
    assert res.status_code == 201
    task = res.json()
    tid = task["id"]

    # update task
    res_up = client.put(f"/api/tasks/{tid}", json={"completed": True})
    assert res_up.status_code == 200
    assert res_up.json()["completed"] is True

    # delete task
    res_del = client.delete(f"/api/tasks/{tid}")
    assert res_del.status_code == 204

    # confirm gone
    res_get = client.get(f"/api/tasks/{tid}")
    assert res_get.status_code == 404

def test_products_crud():
    # create
    res = client.post("/api/products", json={"name":"Prod X","price":9.99})
    assert res.status_code == 201
    pid = res.json()["id"]

    # list
    res_list = client.get("/api/products")
    assert res_list.status_code == 200
    assert any(p["id"]==pid for p in res_list.json())

    # get
    res_get = client.get(f"/api/products/{pid}")
    assert res_get.status_code == 200

    # delete
    res_del = client.delete(f"/api/products/{pid}")
    assert res_del.status_code == 204
