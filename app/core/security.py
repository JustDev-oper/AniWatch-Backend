from fastapi import Depends, HTTPException, Security
from fastapi.security.api_key import APIKeyHeader
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import settings


API_KEY_NAME = "X-API-KEY"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def get_api_key(api_key_header_value: str = Security(api_key_header)) -> str:
    """Dependency: проверяет заголовок X-API-KEY против настроенной переменной окружения.

    Если переменная окружения `API_KEY` не задана — вернётся 500, т.к. в production
    это небезопасно оставлять пустым.
    """
    expected = settings.api_key

    if not expected:
        # Внезапно — на сервере не настроен API_KEY, следует задать его в Railway Secrets
        raise HTTPException(status_code=500, detail="Server misconfiguration: API_KEY is not set")

    if not api_key_header_value or api_key_header_value != expected:
        raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Invalid or missing API Key")

    return api_key_header_value
