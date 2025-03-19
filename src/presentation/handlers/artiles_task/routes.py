import traceback
from typing import Annotated, List

from fastapi import APIRouter, Query, HTTPException
from fastapi.params import Depends
from loguru import logger
from pydantic import TypeAdapter

from src.application.article_tasks import create_article_task, get_task, get_tasks_page
from src.domain.events.publisher import BasePublisher
from src.domain.repositories.article_task import ArticleTaskRepository
from src.infrastructure.depends.events import get_rabbitmq_publisher
from src.infrastructure.depends.repo import get_task_article_repo
from src.presentation.handlers.artiles_task.models import BasePageIterationQuery, CreateTaskRequest, CreateTaskResponse, \
    StatusTaskResponse, TaskInfoResponse, TaskInfoListResponse

router = APIRouter(
    prefix='/task',
    tags=['articles task']
)


@router.post('')
async def create_task_handler(
        data: CreateTaskRequest,
        article_repo: ArticleTaskRepository = Depends(get_task_article_repo),
        publisher: BasePublisher = Depends(get_rabbitmq_publisher),
):
    try:
        task = await create_article_task(
            text=data.text,
            title=data.title,
            article_repo=article_repo,
            publisher=publisher,
        )
        return CreateTaskResponse(task_id=str(task.id))
    except Exception as e:
        traceback.print_exc()
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='непредвиденная ошибка')


@router.get('/status/{task_id}')
async def get_task_status_handler(
        task_id: str,
        article_repo: ArticleTaskRepository = Depends(get_task_article_repo),
):
    try:
        task = await get_task(
            task_id=task_id,
            article_repo=article_repo
        )
        return StatusTaskResponse(
            task_id=task_id,
            status=task.status
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='непредвиденная ошибка')


@router.get('/info/{task_id}')
async def get_task_result_handler(
        task_id: str,
        article_repo: ArticleTaskRepository = Depends(get_task_article_repo),

):
    try:
        task = await get_task(
            task_id=task_id,
            article_repo=article_repo
        )
        return TaskInfoResponse(**task.to_dict())
    except Exception as e:
        traceback.print_exc()
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='непредвиденная ошибка')


@router.get('')
async def get_task_list_handler(
        data: Annotated[BasePageIterationQuery, Query()],
        article_repo: ArticleTaskRepository = Depends(get_task_article_repo),
) -> TaskInfoListResponse:
    try:
        res = await get_tasks_page(
            page=data.page,
            size=data.size,
            article_repo=article_repo
        )
        print(res)
        ta = TypeAdapter(List[TaskInfoResponse])
        res = ta.validate_python(res, from_attributes=True)
        return TaskInfoListResponse(
            meta=data,
            items=res
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='непредвиденная ошибка')
