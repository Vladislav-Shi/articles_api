import os
import platform
import time

import uvicorn
from loguru import logger

from src.infrastructure.config import settings
from src.main import app

if platform.system() != 'Windows':
    os.environ['TZ'] = 'Europe/Moscow'
    time.tzset()


def run_server():
    logger.info(f'swagger url http://{settings.HOST}:{settings.PORT}/docs')
    uvicorn.run(
        app=app,
        host='0.0.0.0',
        log_level='warning' if not settings.DEBUG else 'info',
        port=settings.PORT,
    )


if __name__ == '__main__':
    run_server()
