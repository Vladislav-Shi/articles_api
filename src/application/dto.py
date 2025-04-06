from typing import List

from pydantic import BaseModel

from src.domain.models.article_task import ArticleTask


class ArticlesTaskList(BaseModel):
    count: int
    items: List[ArticleTask]

    class Config:
        arbitrary_types_allowed = True