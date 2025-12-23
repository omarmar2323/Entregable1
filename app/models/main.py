from fastapi import FastAPI

from app.api.tasks_router import router as tasks_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=settings.app_description,
)

app.include_router(tasks_router)



