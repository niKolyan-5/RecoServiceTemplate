from typing import List

import numpy as np
from fastapi import APIRouter, Depends, FastAPI, HTTPException, Request
from fastapi.security.api_key import APIKey
from pydantic import BaseModel

from ordinarypopular import dataset, ordinary_popular
from service.api.exceptions import UserNotFoundError
from service.log import app_logger
from service.models import (
    model_names,  # импортируем список верных имен моделей
)
from tests.api.test_views import test_api_key


class RecoResponse(BaseModel):
    user_id: int
    items: List[int]


router = APIRouter()


@router.get(
    path="/health",
    tags=["Health"],
)
async def health() -> str:
    return "I am alive"


@router.get(
    path="/reco/{model_name}/{user_id}",
    tags=["Recommendations"],
    response_model=RecoResponse,
)
async def get_reco(
    request: Request,
    model_name: str,
    user_id: int,
    api_key: APIKey = Depends(test_api_key)
) -> RecoResponse:
    if model_name in model_names:
        app_logger.info(f"Request for model: {model_name}, user_id: {user_id}")
    else:
        # исключение, если имя модели не является верным
        raise HTTPException(status_code=404, detail="Model is not valid")

    if user_id > 10**9:
        raise UserNotFoundError(error_message=f"User {user_id} not found")

    k_recs = request.app.state.k_recs
    # выдача рекомендаций
    try:
        reco = ordinary_popular.recommend(
            np.array([user_id]),
            dataset=dataset,
            k=k_recs,
            filter_viewed=False  # True - throw away some items for each user
        )['item_id'].to_list()
    except Exception:
        reco = list(range(k_recs))
    finally:
        return RecoResponse(user_id=user_id, items=reco)


def add_views(app: FastAPI) -> None:
    app.include_router(router)
