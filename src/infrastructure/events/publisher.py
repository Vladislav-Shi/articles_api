import json

import aio_pika
from loguru import logger

from src.domain.events.publisher import BasePublisher


class RabbitPublisher(BasePublisher):
    def __init__(
            self,
            host: str,
            exchange: str
    ):
        self.host = host
        self.exchange = exchange
        self.connection: aio_pika.abc.AbstractRobustConnection | None = None
        self.channel: aio_pika.abc.AbstractChannel | None = None
        self.exchange_obj: aio_pika.abc.AbstractExchange | None = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.host)
        self.channel = await self.connection.channel()
        self.exchange_obj = await self.channel.declare_exchange(
            self.exchange,
            aio_pika.ExchangeType.TOPIC,
            durable=True
        )
        await self.initialize_queues()

    async def initialize_queues(self):
        if not self.channel:
            raise RuntimeError('Соеденение с RabbitMQ не найдено')
        article_task_queue = await self.channel.declare_queue(
            "article_task",
            durable=True
        )
        await article_task_queue.bind(self.exchange_obj, routing_key="article_task")

    async def publish_article_task(self, task_id: str):
        if not self.channel:
            raise RuntimeError('Соеденение с RabbitMQ не найдено')
        message_body = json.dumps({"task_id": task_id}).encode()
        message = aio_pika.Message(
            body=message_body,
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT  # Сообщение будет сохранено на диск
        )
        await self.exchange_obj.publish(message, routing_key="article_task")
        logger.info(f"Sent task ID: {task_id} to queue: 'article_task'")


    async def disconnect(self):
        if self.connection:
            await self.connection.close()
