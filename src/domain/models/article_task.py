from datetime import datetime
from uuid import UUID, uuid4
from enum import Enum

from src.domain.exeptions import ValidationError


class PiplineResult:
    pipelines: dict
    errors: dict | None

    def __init__(self, pipelines: dict, errors: dict | None = None, **kwargs):
        self.pipelines = pipelines
        self.errors = errors


    def to_dict(self) -> dict:
        return {
            'pipelines': self.pipelines,
            'errors': self.errors,
        }


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
            pipline_result: PiplineResult = None
    ):
        self.id = id if id else uuid4()
        if isinstance(id, str):
            self.id = UUID(self.id)
        self.text = text
        self.title = title
        self.status = status
        self.created_at = created_at if completed_at else datetime.now()
        self.completed_at = completed_at
        if isinstance(pipline_result, dict):
            pipline_result = PiplineResult(**pipline_result)
        self.pipline_result = pipline_result

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

    def to_dict(self) -> dict:
        return dict(
            title=self.title,
            id=str(self.id),
            status=self.status,
            text=self.text,
            pipline_result=self.pipline_result.to_dict() if self.pipline_result else None,
            completed_at=self.completed_at,
            created_at=self.created_at,
        )

    def __str__(self):
        return f'ArticleTask(id={self.id})'

    def __repr__(self):
        return f'ArticleTask(id={self.id})'

