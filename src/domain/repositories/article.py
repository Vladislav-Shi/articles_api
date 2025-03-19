from abc import ABC, abstractmethod



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
