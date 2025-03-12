from typing import List, Dict

from pydantic import BaseModel


class PredictTextRequest(BaseModel):
    text: str


class PrettyPredictResponse(BaseModel):
    classes: List[str]


class CategoryResponse(BaseModel):
    categories: Dict[str, int]
