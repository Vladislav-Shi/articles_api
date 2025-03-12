from src.infrastructure.config import settings
from src.infrastructure.service_api.predict_api.service import PredictRequester, PredictRequesterConfig


def get_avito_profile_requester() -> PredictRequester:
    return PredictRequester(
        config=PredictRequesterConfig(
            base_url=settings.service.PREDICT_URL,
            secret_key=settings.service.PREDICT_SECRET,
        )
    )

