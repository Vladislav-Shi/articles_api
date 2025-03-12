from fastapi import FastAPI

from src.presentation.handlers.articles.routes import router
from src.presentation.handlers.artiles_task.routes import router as articles_task_router


def include_routes(app: FastAPI) -> None:
    app.include_router(router)
    app.include_router(articles_task_router)
