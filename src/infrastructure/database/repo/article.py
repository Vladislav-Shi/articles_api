from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.article import Article
from src.domain.repositories.article import ArticleRepository
from src.infrastructure.database.mappers import ArticleMapper
from src.infrastructure.database.models import ArticleTable


class ArticleRepo(ArticleRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, article_id: str) -> Article | None:
        query = select(ArticleTable).filter(
            ArticleTable.id == article_id
        )
        result = (await self.session.scalars(query)).first()
        if result:
            return ArticleMapper.to_domain(result)
        return None

    async def save(self, article: Article) -> None:
        orm_article = ArticleMapper.to_orm(article)
        self.session.add(orm_article)

    async def update(self, article: Article) -> None:
        orm_article = ArticleMapper.to_orm(article)
        await self.session.merge(orm_article)



