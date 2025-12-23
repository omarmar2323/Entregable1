from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_crear_tarea():
    nueva_tarea = {
        "title": "tarea_de_prueba",
        "description": "descripcion_de_prueba",
        "priority": "alta",
        "effort_hours": 2.5,
        "status": "pendiente",
        "assigned_to": "usuario_prueba",
    }
    response = client.post("/tasks", json=nueva_tarea)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == nueva_tarea["title"]


def test_leer_todas_las_tareas():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_leer_una_tarea():
    nueva_tarea = {
        "title": "tarea_para_leer",
        "description": "descripcion",
        "priority": "media",
        "effort_hours": 1.0,
        "status": "pendiente",
        "assigned_to": "usuario_leer",
    }
    post_response = client.post("/tasks", json=nueva_tarea)
    task_id = post_response.json()["id"]

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["id"] == task_id


def test_actualizar_tarea():
    nueva_tarea = {
        "title": "tarea_para_actualizar",
        "description": "descripcion",
        "priority": "baja",
        "effort_hours": 3.0,
        "status": "pendiente",
        "assigned_to": "usuario_actualizar",
    }
    post_response = client.post("/tasks", json=nueva_tarea)
    task_id = post_response.json()["id"]

    tarea_actualizada = {
        "title": "tarea_actualizada",
        "description": "descripcion_actualizada",
        "priority": "alta",
        "effort_hours": 5.0,
        "status": "en_progreso",
        "assigned_to": "usuario_actualizado",
    }
    put_response = client.put(f"/tasks/{task_id}", json=tarea_actualizada)
    assert put_response.status_code == 200
    data = put_response.json()
    assert data["title"] == tarea_actualizada["title"]
    assert data["status"] == tarea_actualizada["status"]


def test_eliminar_tarea():
    nueva_tarea = {
        "title": "tarea_para_eliminar",
        "description": "descripcion",
        "priority": "bloqueante",
        "effort_hours": 8.0,
        "status": "pendiente",
        "assigned_to": "usuario_eliminar",
    }
    post_response = client.post("/tasks", json=nueva_tarea)
    task_id = post_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404



