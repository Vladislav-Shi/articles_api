from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from starlette.middleware.cors import CORSMiddleware

from src.presentation.handlers import include_routes

app = FastAPI()
include_routes(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    # Стандартная схема
    openapi_schema = get_openapi(
        title='Articles API',
        version='1.0.0',
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@app.get('/ping')
async def ping():
    return {'message': 'OK'}
