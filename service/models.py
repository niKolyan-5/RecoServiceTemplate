import typing as tp

from pydantic import BaseModel

# условный список зарегистрированных моделей
model_names = ['some_model', 'mmm', 'nnn', 'LightFM_warp_64_05_16', 'LightFM', 'LGBMRankerModel']


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None