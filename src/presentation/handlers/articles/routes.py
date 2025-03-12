from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from loguru import logger

from src.application.artiles import predict_article_category, get_predict_categories
from src.infrastructure.depends.service_api import get_avito_profile_requester
from src.infrastructure.service_api.predict_api.service import PredictRequester
from src.presentation.handlers.articles.models import PrettyPredictResponse, PredictTextRequest, CategoryResponse

router = APIRouter(
    prefix='/articles',
    tags=['articles']
)


@router.post('/predict')
async def predict_articles_category_handler(
        data: PredictTextRequest,
        predict_api: PredictRequester = Depends(get_avito_profile_requester)
) -> PrettyPredictResponse:
    try:
        res = await predict_article_category(
            text=data.text,
            predict_api=predict_api
        )
        return PrettyPredictResponse.model_validate(res)
    except Exception as e:
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='Непредвиденная ошибка')


@router.get('/predict/categories')
async def get_predict_categories_handler(
        predict_api: PredictRequester = Depends(get_avito_profile_requester)
) -> CategoryResponse:
    try:
        res = await get_predict_categories(
            predict_api=predict_api
        )
        return CategoryResponse.model_validate(res)
    except Exception as e:
        logger.error(f'{e=}')
        raise HTTPException(status_code=400, detail='Непредвиденная ошибка')
