from src.domain.models.article import Article
from src.infrastructure.database.models import ArticleTable


class ArticleMapper:
    @staticmethod
    def to_orm(article: Article) -> ArticleTable:
        return ArticleTable(
            id=article.id,
            title=article.title,
            text=article.text,
            created_at=article.created_at
        )

    @staticmethod
    def to_domain(orm_article: ArticleTable) -> Article:
        return Article(
            id=orm_article.id,
            title=orm_article.title,  # Здесь должен быть RussianText VO
            text=orm_article.text,
            category=orm_article.category,
            created_at=orm_article.create_at
        )
