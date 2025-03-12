from typing import Annotated

from fastapi import APIRouter, Query

from src.presentation.handlers.artiles_task.models import BasePageIterationQuery

router = APIRouter(
    prefix='/task',
    tags=['articles task']
)


@router.post('')
async def create_task_handler():
    pass


@router.get('/status/{task_id}')
async def get_task_status_handler(task_id: str):
    pass


@router.get('/result/{task_id}')
async def get_task_result_handler(task_id: str):
    pass


@router.get('')
async def get_task_list_handler(
        data: Annotated[BasePageIterationQuery, Query()]
):
    pass
