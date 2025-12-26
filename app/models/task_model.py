from typing import Literal, Annotated
from pydantic import BaseModel, ConfigDict, Field, StrictFloat


class task(BaseModel):
    """
    Modelo que representa una tarea en el sistema.

    Atributos:
        id (int | None): ID autoincremental de la tarea (se asigna automáticamente al crearla).
        title (str): Título breve que resume la tarea.
        description (str): Descripción detallada de la tarea.
        priority (str): Prioridad de la tarea. Solo permite: 'baja', 'media', 'alta', 'bloqueante'.
        effort_hours (float): Estimación de esfuerzo en horas para resolver la tarea.
        status (str): Estado de la tarea. Solo permite: 'pendiente', 'en_progreso', 'en_revision', 'completada'.
        assigned_to (str): Persona a la que está asignada la tarea.

    Métodos:
        to_dict(): Devuelve un diccionario con los datos de la tarea.
        from_dict(data): Crea una instancia de `task` a partir de un diccionario.
    """
    # Ejemplo para Swagger/OpenAPI (aparece precargado en /docs)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "tarea_de_ejemplo",
                "description": "descripcion_de_la_tarea",
                "priority": "alta",
                "effort_hours": 4.5,
                "status": "pendiente",
                "assigned_to": "juan_perez"
            }
        }
    )
    id: int | None = None
    title: str
    description: str
    priority: Literal["baja", "media", "alta", "bloqueante"]
    effort_hours: Annotated[StrictFloat, Field(gt=0)]
    status: Literal["pendiente", "en_progreso", "en_revision", "completada"]
    assigned_to: str

    def to_dict(self) -> dict:
        """Devuelve un diccionario serializable con los datos de la tarea."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "task":
        """Crea una tarea a partir de un diccionario de datos."""
        return cls(**data)



