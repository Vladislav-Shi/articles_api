from src.infrastructure.config import settings
from src.infrastructure.events.publisher import RabbitPublisher


async def get_rabbitmq_publisher() -> RabbitPublisher:
    publisher = RabbitPublisher(
        host=settings.RABBIT_URL,
        exchange=settings.EXCHANGE_RABBIT_NAME,
    )

    await publisher.connect()

    try:
        yield publisher
    finally:
        await publisher.disconnect()
