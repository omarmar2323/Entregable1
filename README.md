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

## ubicacion_de_clases

- Clase Task: ubicada en `app/models/task_model.py`. Definida como `class task(BaseModel)`, representa el esquema de una tarea y provee:
  - `to_dict()`: convierte la instancia de `task` a diccionario serializable.
  - `from_dict(data)`: crea una instancia de `task` a partir de un diccionario.

- Clase TaskManager: ubicada en `app/services/task_manager.py`. Definida como `class task_manager`, gestiona el almacenamiento en `data/tasks_json.json` y expone métodos estáticos:
  - `load_tasks()`: carga tareas desde el JSON y las valida.
  - `save_tasks(tasks)`: guarda la lista de tareas en el JSON.
  - `create_task(new_task)`: crea una nueva tarea con ID autoincremental.
  - `get_all_tasks()`: devuelve todas las tareas.
  - `get_task_by_id(task_id)`: devuelve una tarea por ID.
  - `update_task(task_id, updated_task)`: actualiza una tarea existente.
  - `delete_task(task_id)`: elimina una tarea por ID.

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

## errores_comunes (índice_rápido)

- [errores_de_validación_422](#errores_de_validación_422)
- [valores_permitidos_y_validación](#valores_permitidos_y_validación)
- [errores_específicos_effort_hours](#errores_específicos_effort_hours)
- [errores_formato_campos_string](#errores_formato_campos_string)

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

#### errores_de_validación_422

Errores de validación (422 Unprocessable Content):

- Si faltan campos requeridos en el cuerpo, la API devuelve un objeto con `msg` indicando cuáles faltan.
- Ejemplo de respuesta cuando faltan campos:

```json
{
  "msg": "Faltan los siguientes campos requeridos: description, priority, effort_hours, status, assigned_to"
}
```

Notas:
- El campo `id` no debe enviarse; se asigna automáticamente.
- Los valores de `priority` y `status` deben corresponder a los permitidos por el esquema.

#### valores_permitidos_y_validación

Valores permitidos y validación:

- `priority`: baja, media, alta, bloqueante
- `status`: pendiente, en_progreso, en_revision, completada

Si se envía un valor inválido, la API responde 422 (Unprocessable Content) con errores de validación estándar en `detail`.

Ejemplo de solicitud inválida (priority no permitido):

```json
{
  "title": "tarea_invalida",
  "description": "desc",
  "priority": "urgente",
  "effort_hours": 1.0,
  "status": "pendiente",
  "assigned_to": "alguien"
}
```

Ejemplo de respuesta (resumen):

```json
{
  "detail": [
    {
      "loc": ["body", "priority"],
      "msg": "Input should be 'baja' or 'media' or 'alta' or 'bloqueante'",
      "type": "literal_error"
    }
  ]
}
```

#### errores_específicos_effort_hours

Errores específicos para `effort_hours`:

- No numérico:

  Solicitud (ejemplo):

  ```json
  {
    "title": "tarea",
    "description": "desc",
    "priority": "alta",
    "effort_hours": "hola",
    "status": "pendiente",
    "assigned_to": "usuario"
  }
  ```

  Respuesta:

  ```json
  {
    "msg": "effort_hours debe ser numérico",
    "detail": [
      {
        "type": "float_type",
        "loc": ["body", "effort_hours"],
        "msg": "Input should be a valid number",
        "input": "hola"
      }
    ]
  }
  ```

- Menor o igual a cero:

  Solicitud (ejemplo):

  ```json
  {
    "title": "tarea",
    "description": "desc",
    "priority": "alta",
    "effort_hours": 0,
    "status": "pendiente",
    "assigned_to": "usuario"
  }
  ```

  Respuesta:

  ```json
  {
    "msg": "effort_hours debe ser mayor a 0",
    "detail": [
      {
        "type": "greater_than",
        "loc": ["body", "effort_hours"],
        "msg": "Input should be greater than 0",
        "input": 0
      }
    ]
  }
  ```

- JSON inválido (token sin comillas):

  Solicitud (ejemplo):

  ```json
  {"title":"x","description":"y","priority":"alta","effort_hours": ew, "status":"pendiente","assigned_to":"z"}
  ```

  Respuesta:

  ```json
  {
    "msg": "effort_hours debe ser numérico",
    "detail": [
      {
        "type": "json_invalid",
        "loc": ["body", 95],
        "msg": "JSON decode error",
        "ctx": {"error": "Expecting value"}
      }
    ]
  }
  ```

  #### errores_formato_campos_string

  Errores de formato en campos string (JSON inválido, valores sin comillas):

  - Si un campo de texto del esquema (`title`, `description`, `priority`, `status`, `assigned_to`) se envía sin comillas dobles en un JSON inválido, la API devuelve un 422 con un mensaje claro indicando el formato incorrecto.

  Ejemplos:

  - Priority sin comillas:

    Solicitud:

    ```json
    {"title":"x","description":"y","priority": urgente, "effort_hours": 1.0, "status":"pendiente","assigned_to":"z"}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "priority tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```

  - Title sin comillas:

    Solicitud:

    ```json
    {"title": x, "description":"y","priority":"alta", "effort_hours": 1.0, "status":"pendiente","assigned_to":"z"}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "title tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```

  - Status sin comillas:

    Solicitud:

    ```json
    {"title":"x","description":"y","priority":"alta", "effort_hours": 1.0, "status": pendiente, "assigned_to":"z"}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "status tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```

  Caso combinado (sin confusión con effort_hours):

  - Priority sin comillas y effort_hours válido:

    Solicitud:

    ```json
    {"title":"x","description":"y","priority": alta, "effort_hours": 4.5, "status":"pendiente","assigned_to":"z"}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "priority tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```
    Nota: No agrega "effort_hours debe ser numérico" porque `effort_hours` es un número válido (4.5).

  - Description sin comillas:

    Solicitud:

    ```json
    {"title":"x","description": descripcion_larga, "priority":"alta", "effort_hours": 1.0, "status":"pendiente","assigned_to":"z"}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "description tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```

  - Assigned_to sin comillas:

    Solicitud:

    ```json
    {"title":"x","description":"y","priority":"alta", "effort_hours": 1.0, "status":"pendiente","assigned_to": usuario_sin_comillas}
    ```

    Respuesta (resumen):

    ```json
    {
      "msg": "assigned_to tiene formato inválido: debe ser texto entre comillas dobles",
      "detail": [
        { "type": "json_invalid", "loc": ["body", ...], "msg": "JSON decode error" }
      ]
    }
    ```

Nota de datos legados:
- Si existen tareas inválidas en `data/tasks_json.json` (por ejemplo, `effort_hours`=0), el sistema las omite al cargar para evitar errores.

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

Los tests incluyen la validación del mensaje de error en la creación de tareas cuando faltan campos requeridos.


