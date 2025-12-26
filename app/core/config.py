from functools import lru_cache

from pydantic import BaseModel


class app_settings(BaseModel):
    """
    Configuración principal de la aplicación FastAPI.

    Atributos:
        app_name (str): Nombre de la aplicación.
        app_version (str): Versión de la API.
        app_description (str): Descripción breve usada en Swagger/OpenAPI.
    """
    app_name: str = "gestor_de_tareas_fastapi"
    app_version: str = "1.0.0"
    app_description: str = (
        "api_rest_para_la_gestion_de_tareas_de_usuario_con_almacenamiento_en_json"
    )


@lru_cache
def get_settings() -> app_settings:
    """
    Devuelve la configuración de la aplicación como singleton (con cache).
    Returns:
        app_settings: Instancia única de configuración.
    """
    return app_settings()



