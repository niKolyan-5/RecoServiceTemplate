from http import HTTPStatus

from fastapi import HTTPException, Security
from fastapi.security.api_key import APIKeyCookie, APIKeyHeader, APIKeyQuery
from starlette.status import HTTP_403_FORBIDDEN
from starlette.testclient import TestClient

from service.settings import ServiceConfig

GET_RECO_PATH = "/reco/{model_name}/{user_id}?api_key={api_key}"

API_KEY = "FFF"
API_KEY_NAME = "api_key"
COOKIE_DOMAIN = "localtest.me"


def test_health(
    client: TestClient,
) -> None:
    with client:
        response = client.get("/health")
    assert response.status_code == HTTPStatus.OK


def test_get_reco_success(
    client: TestClient,
    service_config: ServiceConfig,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(
        model_name="some_model",
        user_id=user_id,
        api_key="FFF")
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.OK
    response_json = response.json()
    assert response_json["user_id"] == user_id
    assert len(response_json["items"]) == service_config.k_recs
    assert all(isinstance(item_id, int) for item_id in response_json["items"])


def test_get_reco_for_unknown_user(
    client: TestClient,
) -> None:
    user_id = 10**10
    path = GET_RECO_PATH.format(
        model_name="some_model",
        user_id=user_id,
        api_key="FFF")
    with client:
        response = client.get(path)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()["errors"][0]["error_key"] == "user_not_found"


async def test_api_key(
    api_key_query: str = Security(APIKeyQuery(name=API_KEY_NAME,
                                              auto_error=False)),
    api_key_header: str = Security(APIKeyHeader(name=API_KEY_NAME,
                                                auto_error=False)),
    api_key_cookie: str = Security(APIKeyCookie(name=API_KEY_NAME,
                                                auto_error=False)),
):

    if api_key_query == API_KEY:
        return api_key_query
    if api_key_header == API_KEY:
        return api_key_header
    if api_key_cookie == API_KEY:
        return api_key_cookie
    raise HTTPException(
        status_code=HTTP_403_FORBIDDEN,
        detail="There is no key or it is wrong"
    )


# здесь и далее тесты на верное/неверное имя модели
def test_valid_model_name(
    client: TestClient,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(
        model_name="some_model",
        user_id=user_id,
        api_key="FFF")
    with client:
        response = client.get(path)
    assert response.status_code == 200
    assert response.json() == {
        "user_id": user_id,
        "items": list(range(10))
    }


def test_invalid_model_name(
    client: TestClient,
) -> None:
    user_id = 123
    path = GET_RECO_PATH.format(
        model_name="invalid_model",
        user_id=user_id,
        api_key="FFF")
    with client:
        response = client.get(path)
    assert response.status_code == 404