# gestor_de_tareas_fastapi

Aplicación FastAPI para la **gestión de tareas de usuario**, donde cada tarea se almacena en un archivo JSON dentro de la carpeta `data/`.  
La API expone endpoints CRUD para crear, leer, actualizar y eliminar tareas, siguiendo una arquitectura modular.

## objetivo_del_proyecto

- Gestionar tareas con los campos:
  - `id`
  - `title`
  - `description`
  - `priority` (baja, media, alta, bloqueante)
  - `effort_hours`
  - `status` (pendiente, en_progreso, en_revision, completada)
  - `assigned_to`
- Almacenar las tareas en `data/tasks_json.json` en un diccionario cuya clave principal es `Tasks`.
- Gestionar la lógica de `id` como un campo independiente dentro del JSON.

## estructura_del_proyecto

```text
project_root/
│── app/
│   ├── main.py
│   ├── api/
│   │   └── tasks_router.py
│   ├── services/
│   │   └── task_manager.py
│   ├── models/
│   │   └── task_model.py
│   └── core/
│       └── config.py
│
│── data/
│   └── tasks_json.json
│
│── tests/
│   └── test_tasks_api.py
│
│── requirements.txt
│── .gitignore
│── README.md
```

> Nota: el proyecto sigue estrictamente el estilo `snake_case` para clases, variables, métodos, archivos y carpetas.

## instalación_y_ejecución

### 1. crear_entorno_virtual

Desde la raíz del proyecto:

```bash
python -m venv venv
```

Activar el entorno (Windows PowerShell):

```bash
.\venv\Scripts\Activate.ps1
```

### 2. instalar_dependencias

```bash
pip install -r requirements.txt
```

### 3. ejecutar_la_api

```bash
uvicorn app.main:app --reload
```

La documentación Swagger estará disponible en:

- `http://127.0.0.1:8000/docs` (Swagger UI)
- `http://127.0.0.1:8000/redoc` (ReDoc)

## ejemplo_de_uso

### crear_una_tarea (POST `/tasks`)

```json
{
  "title": "tarea_de_ejemplo",
  "description": "descripcion_de_la_tarea",
  "priority": "alta",
  "effort_hours": 4.5,
  "status": "pendiente",
  "assigned_to": "juan_perez"
}
```

### leer_todas_las_tareas (GET `/tasks`)

Devuelve una lista con todas las tareas almacenadas.

### leer_una_tarea (GET `/tasks/{id}`)

Devuelve la tarea con el `id` indicado si existe.

### actualizar_una_tarea (PUT `/tasks/{id}`)

Recibe un cuerpo JSON con el mismo esquema que la creación y reemplaza los datos de la tarea indicada.

### eliminar_una_tarea (DELETE `/tasks/{id}`)

Elimina la tarea con el `id` indicado y devuelve una confirmación.

## pruebas_con_pytest

Para ejecutar las pruebas automatizadas:

```bash
pytest
```


