from typing import Union, Literal

from .model import Item, Zone, Stage, Matrix

T_Server = Literal["cn", "kr", "us", "jp"]
T_Lang = Literal["zh", "ko", "en", "ja"]
T_Query = Literal["item", "stage", "exact"]
T_Model = Union[Item, Stage, Zone, Matrix]
T_Respond = Literal["item", "stage", "zone", "matrix"]
T_Sorted_Key = Literal["percentage", "apPPR"]
T_Filter_Mode = Literal["all", "only_open", "only_close"]

lang_map = {"cn": "zh", "kr": "ko", "us": "en", "jp": "ja"}
