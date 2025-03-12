from typing import List, TypedDict, Dict

from pydantic import BaseModel


class BaseResponse(TypedDict):
    message: str


class PredictTextRequest(TypedDict):
    text: str


class PrettyPredictResponse(TypedDict):
    classes: List[str]


class CategoryResponse(TypedDict):
    categories: Dict[str, int]
