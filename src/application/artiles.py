from src.infrastructure.service_api.predict_api.service import PredictRequester


async def predict_article_category(
        text: str,
        predict_api: PredictRequester
):
    res = await predict_api.predict_pretty({'text': text})
    return res


async def get_predict_categories(
        predict_api: PredictRequester
):
    res = await predict_api.get_categories()
    return res
