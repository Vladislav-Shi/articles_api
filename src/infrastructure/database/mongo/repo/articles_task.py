from typing import List

from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.models.article_task import ArticleTask
from src.domain.repositories.article_task import ArticleTaskRepository


class MongoArticleTaskRepository(ArticleTaskRepository):

    def _replace_id_from_db(self, document: dict) -> ArticleTask:
        document['id'] = document['_id']
        del document['_id']
        return ArticleTask(
            **document
        )

    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    async def get_by_id(self, task_id: str) -> ArticleTask | None:
        document = await self.collection.find_one({"_id": task_id})
        if not document:
            return None
        document = self._replace_id_from_db(document)
        return document

    async def save(self, article: ArticleTask) -> None:
        document = article.to_dict()
        document['_id'] = document['id']
        del document['id']
        await self.collection.insert_one(document)

    async def update(self, article: ArticleTask) -> None:
        pass

    async def list(self, offset: int, limit: int, **kwargs) -> List[ArticleTask]:
        cursor = self.collection.find().skip(offset).limit(limit)
        tasks = await cursor.to_list(length=limit)
        tasks = [self._replace_id_from_db(i) for i in tasks]
        return tasks
