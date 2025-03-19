from datetime import datetime

from src.domain.events.publisher import BasePublisher
from src.domain.models.article_task import ArticleTask, ArticleStatusEnum
from src.domain.repositories.article_task import ArticleTaskRepository
from src.exceptions import NotExistException


async def create_article_task(
        text: str,
        title: str | None,
        article_repo: ArticleTaskRepository,
        publisher: BasePublisher,
) -> ArticleTask:
    article_task = ArticleTask(
        created_at=datetime.now(),
        text=text,
        title=title,
        status=ArticleStatusEnum.WAITING,
    )
    await article_repo.save(article_task)
    await publisher.publish_article_task(task_id=str(article_task.id))
    return article_task


async def get_task(
        task_id: str,
        article_repo: ArticleTaskRepository,
):
    res = await article_repo.get_by_id(task_id=task_id)
    if res is None:
        raise NotExistException()
    return res


async def get_tasks_page(
        article_repo: ArticleTaskRepository,
        page: int = 1,
        size: int = 10,
):
    if page < 1 or size < 1:
        raise ValueError()
    res = await article_repo.list(
        limit=size,
        offset=(page - 1) * size
    )
    return res
