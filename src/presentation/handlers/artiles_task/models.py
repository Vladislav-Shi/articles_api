from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    text: str
    title: str | None = None


class CreateTaskResponse(BaseModel):
    task_id: str


class StatusTaskResponse(BaseModel):
    task_id: str
    status: str


class PiplineResult(BaseModel):
    errors: dict | None
    pipelines: dict


class TaskInfoResponse(BaseModel):
    id: str | UUID
    title: str | None = None
    status: str
    created_at: datetime
    completed_at: datetime | None
    pipline_result: PiplineResult | None


class BasePageIterationQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1)

class BasePageIterationResponse(BasePageIterationQuery):
    count: int

class TaskInfoListResponse(BaseModel):
    meta: BasePageIterationResponse
    items: List[TaskInfoResponse]
