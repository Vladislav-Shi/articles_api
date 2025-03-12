from pydantic import BaseModel, Field


class BasePageIterationQuery(BaseModel):
    page: int = Field(default=1, ge=1)
    size: int = Field(default=10, ge=1)
