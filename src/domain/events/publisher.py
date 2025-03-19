from abc import ABC, abstractmethod


class BasePublisher(ABC):

    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def publish_article_task(self, task_id: str):
        pass

    @abstractmethod
    async def disconnect(self):
        pass