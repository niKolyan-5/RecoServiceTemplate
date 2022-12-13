import typing as tp

from pydantic import BaseModel

# условный список зарегистрированных моделей
model_names = ['some_model', 'ordinary_popular', 'userknn']


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None
