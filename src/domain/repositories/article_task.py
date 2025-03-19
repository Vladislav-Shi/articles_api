from abc import ABC, abstractmethod
from typing import List

from src.domain.models.article_task import ArticleTask


class ArticleTaskRepository(ABC):

    @abstractmethod
    async def get_by_id(self, task_id: str) -> ArticleTask | None:
        pass

    @abstractmethod
    async def save(self, article: ArticleTask) -> None:
        pass

    @abstractmethod
    async def update(self, article: ArticleTask) -> None:
        pass

    @abstractmethod
    async def list(self, offset: int, limit: int, **kwargs) -> List[ArticleTask]:
        pass
