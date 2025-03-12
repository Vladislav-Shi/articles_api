from abc import ABC, abstractmethod

from src.domain.models.article import Article


class ArticleRepository(ABC):
    @abstractmethod
    async def get_by_id(self, article_id: str) -> Article | None:
        pass

    @abstractmethod
    async def save(self, article: Article) -> None:
        pass

    @abstractmethod
    async def update(self, article: Article) -> None:
        pass
