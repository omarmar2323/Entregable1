from functools import lru_cache

from pydantic import BaseModel


class app_settings(BaseModel):
    app_name: str = "gestor_de_tareas_fastapi"
    app_version: str = "1.0.0"
    app_description: str = (
        "api_rest_para_la_gestion_de_tareas_de_usuario_con_almacenamiento_en_json"
    )


@lru_cache
def get_settings() -> app_settings:
    return app_settings()



