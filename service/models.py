import typing as tp

from pydantic import BaseModel

model_names = ['some_model', 'mmm', 'nnn'] # условный список зарегистрированных моделей


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None