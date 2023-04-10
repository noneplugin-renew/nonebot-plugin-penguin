from typing import Union, Literal

from .model import Item, Zone, Stage, Matrix

T_Server = Literal["cn", "kr", "us", "jp"]
T_Query = Literal["item", "stage", "exact"]
T_Model = Union[Item, Stage, Zone, Matrix]
T_Respond = Literal["item", "stage", "zone", "matrix"]

lang_map = {"cn": "zh", "kr": "ko", "us": "en", "jp": "ja"}
