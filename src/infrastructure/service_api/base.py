import http.client
import json
from typing import Any, Callable, Dict, Literal, Mapping, Optional
from urllib.parse import urlencode, urlparse

import aiohttp
from aiohttp import ClientConnectorError, FormData
from aiohttp.client import _RequestContextManager
from pydantic import AnyHttpUrl, BaseModel

from src.infrastructure.service_api import exceptions as req_exp

METHOD_TYPE = Literal['POST', 'GET', 'PUT', 'DELETE']
RESULT_TYPE = Literal['json', 'text', 'bytes']

ASYNC_HTTP_METHOD_MAPPING: Dict[METHOD_TYPE, Callable[[], _RequestContextManager]] = {
    'GET': aiohttp.ClientSession.get,
    'POST': aiohttp.ClientSession.post,
    'PUT': aiohttp.ClientSession.put,
    'DELETE': aiohttp.ClientSession.delete,
}


class BaseRequesterConfig(BaseModel):
    base_url: AnyHttpUrl
    service_name: str = None
    secret_key: str
    debug: bool = True


class BaseRequester:
    _config: BaseRequesterConfig

    def _get_headers(self) -> Dict[str, Any]:
        return {
            'X-SERVICE-NAME': self._config.service_name,
            'X-SECRET-KEY': self._config.secret_key,
        }

    @property
    def headers(self):
        return self._get_headers()

    def __init__(self, config: BaseRequesterConfig):
        self._config = config

    def _raise_via_status(self, status: int, data: str):
        if status == 400:
            raise req_exp.Error400(data)
        if status == 401:
            raise req_exp.Error401(data)
        if status == 403:
            raise req_exp.Error400(data)
        if status == 405:
            raise req_exp.Error405(data)
        if status == 404:
            raise req_exp.Error404(data)
        if status == 422:
            raise req_exp.Error422(data)
        if status == 429:
            raise req_exp.Error429(data)

    def sync_request(
            self,
            method: METHOD_TYPE,
            url: str,
            params: Mapping[str, str | int] | str | None = None,
            data: Any = None,
            json_: Any = None,
            additional_headers: Optional[dict] = None,
            result_type: RESULT_TYPE = 'json',
    ):
        """Синхронный запрос"""
        headers_ = self.headers
        if additional_headers:
            headers_.update(additional_headers)
        parsed_url = urlparse(str(self._config.base_url))
        conn = (
            http.client.HTTPSConnection(parsed_url.netloc)
            if parsed_url.scheme == 'https'
            else http.client.HTTPConnection(parsed_url.netloc)
        )
        if not url.startswith('/'):
            path = parsed_url.path + url
        else:
            path = url
        if params:
            path += '?' + urlencode(params)

        body = None
        if json_:
            headers_['Content-Type'] = 'application/json'
            body = json.dumps(json_)
        elif data:
            body = urlencode(data)
        try:
            conn.request(method, path, body=body, headers=headers_)
            response = conn.getresponse()
        except (ConnectionRefusedError, ClientConnectorError):
            raise req_exp.ServiceNotFound()
        data = response.read()
        self._raise_via_status(status=response.status, data=data.decode())
        if result_type == 'json':
            data = json.loads(data.decode())
        elif result_type == 'text':
            data = data.decode()
        conn.close()
        return data

    async def async_request(
            self,
            method: METHOD_TYPE,
            url: str,
            params: Mapping[str, str | int] | str | None = None,
            data: FormData | None = None,
            json_: Any = None,
            additional_headers: Optional[dict] = None,
            result_type: RESULT_TYPE = 'json',
    ):
        """Делает ассинхронный запрос в сервис"""
        headers_ = self.headers
        if additional_headers:
            headers_.update(additional_headers)
        async with aiohttp.ClientSession(
                base_url=str(self._config.base_url), headers=headers_
        ) as session:
            # data_ = None
            try:
                async with ASYNC_HTTP_METHOD_MAPPING[method](
                        self=session, url=url, params=params, data=data, json=json_
                ) as response:
                    self._raise_via_status(
                        status=response.status, data=await response.text()
                    )
                    if result_type == 'json':
                        return await response.json()
                    elif result_type == 'text':
                        return await response.text()
                    elif result_type == 'bytes':
                        return await response.content.read()
            except (ConnectionRefusedError, ClientConnectorError):
                raise req_exp.ServiceNotFound()
