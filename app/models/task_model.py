from pydantic import BaseModel
from typing import Literal


class task(BaseModel):
    id: int | None = None
    title: str
    description: str
    priority: Literal["baja", "media", "alta", "bloqueante"]
    effort_hours: float
    status: Literal["pendiente", "en_progreso", "en_revision", "completada"]
    assigned_to: str

    def to_dict(self) -> dict:
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict) -> "task":
        return cls(**data)



