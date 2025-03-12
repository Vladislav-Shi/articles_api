from src.infrastructure.service_api.base import BaseRequester, BaseRequesterConfig
from src.infrastructure.service_api.predict_api.models import PredictTextRequest, BaseResponse, PrettyPredictResponse, \
    CategoryResponse


class PredictRequesterConfig(BaseRequesterConfig):
    service_name: str = 'predict_service'


class PredictRequester(BaseRequester):

    async def predict_pretty(self, data: PredictTextRequest) -> PrettyPredictResponse:
        url = '/api/predict_pretty'
        data_ = data
        res = await self.async_request('POST', url=url, json_=data_)
        return res

    async def get_categories(self) -> CategoryResponse:
        url = '/api/categories'
        res = await self.async_request('GET', url=url)
        return res
