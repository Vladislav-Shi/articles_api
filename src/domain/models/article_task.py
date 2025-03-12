from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from src.domain.exeptions import ValidationError


class ArticleStatusEnum(str, Enum):
    WAITING = 'WAITING'
    PROCESS = 'PROCESS'
    DONE = 'DONE'
    ERROR = 'ERROR'

    def __str__(self):
        return self.value


class ArticleTask:
    def __init__(
            self,
            title: str | None,
            text: str,
            status: ArticleStatusEnum = ArticleStatusEnum.WAITING,
            id: UUID | None = None,
            created_at: datetime | None = None,
            completed_at: datetime | None = None,
    ):
        self.id = id if id else uuid4()
        self.text = text
        self.title = title
        self.status = status
        self.created_at = created_at if completed_at else datetime.now()
        self.completed_at = completed_at

    def validate(self):
        if self.completed_at is None and (
                self.status == ArticleStatusEnum.DONE
                or
                self.status == ArticleStatusEnum.ERROR
        ):
            raise ValidationError(f'Таска имеет статус завершенной "{self.status}", но не имеет время завершения')
        if self.completed_at and (
                self.status == ArticleStatusEnum.WAITING
                or
                self.status == ArticleStatusEnum.PROCESS
        ):
            raise ValidationError(f'Таска имеет время завершения, но не имеет неподходящий статус "{self.status}"')
