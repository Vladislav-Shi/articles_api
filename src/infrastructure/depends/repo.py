from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient

from src.infrastructure.config import settings
from src.infrastructure.database.mongo.repo.articles_task import MongoArticleTaskRepository


async def get_mongo_db():
    mongo_client = AsyncIOMotorClient(settings.MONGO_URL)
    try:
        yield mongo_client[settings.MONGO_DB_NAME]
    finally:
        # Закрываем соединение при завершении работы приложения
        mongo_client.close()


async def get_task_article_repo(
        db: AsyncIOMotorDatabase = Depends(get_mongo_db)
) -> MongoArticleTaskRepository:
    return MongoArticleTaskRepository(db["article_tasks"])
