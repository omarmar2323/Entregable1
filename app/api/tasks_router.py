from typing import List

from fastapi import APIRouter, HTTPException, status

from app.models.task_model import task
from app.services.task_manager import task_manager


router = APIRouter()


@router.post(
    "/tasks",
    response_model=task,
    status_code=status.HTTP_201_CREATED,
    summary="crear_una_tarea",
)
def crear_tarea(task_input: task) -> task:
    return task_manager.create_task(task_input)


@router.get(
    "/tasks",
    response_model=List[task],
    summary="leer_todas_las_tareas",
)
def leer_todas_las_tareas() -> List[task]:
    return task_manager.get_all_tasks()


@router.get(
    "/tasks/{task_id}",
    response_model=task,
    summary="leer_una_tarea",
)
def leer_tarea(task_id: int) -> task:
    existing_task = task_manager.get_task_by_id(task_id)
    if existing_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tarea_no_encontrada",
        )
    return existing_task


@router.put(
    "/tasks/{task_id}",
    response_model=task,
    summary="actualizar_una_tarea",
)
def actualizar_tarea(task_id: int, task_input: task) -> task:
    updated = task_manager.update_task(task_id, task_input)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tarea_no_encontrada",
        )
    return updated


@router.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="eliminar_una_tarea",
)
def eliminar_tarea(task_id: int) -> None:
    deleted = task_manager.delete_task(task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="tarea_no_encontrada",
        )



