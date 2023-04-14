from pydantic import BaseModel

from .types import T_Lang, T_Query, T_Server, T_Sorted_Key, T_Filter_Mode


class Item(BaseModel):
    itemId: str
    name_i18n: dict[str, str]
    spriteCoord: list[int]


class Stage(BaseModel):
    stageId: str
    zoneId: str
    code_i18n: dict[str, str]
    apCost: int
    minClearTime: int


class Zone(BaseModel):
    zoneId: str
    zoneName_i18n: dict[str, str]
    type: str


class Matrix(BaseModel):
    stage: Stage
    zone: Zone
    item: Item
    percentage: float
    apPPR: float
    quantity: int
    times: int
    start: int
    end: int | None

    def export(self, lang) -> dict[str, str | list[int] | float]:
        return dict(
            stage_name=self.stage.code_i18n[lang],
            zone=self.zone.zoneName_i18n[lang],
            item=self.item.name_i18n[lang],
            sprite_coord=self.item.spriteCoord,
            percentage=str(self.percentage) + "%",
            apPPR=self.apPPR,
            quantity=self.quantity,
            times=self.times,
            opening=True if self.end else False,
        )


class Request(BaseModel):
    server: T_Server = "cn"
    type: T_Query
    ids: tuple[str, str] | tuple[str]
    lang: T_Lang = "zh"
    sort_by: T_Sorted_Key = "percentage"
    filter_by: T_Filter_Mode = "only_open"
    ignore_threshold: int = 100
    reverse: bool = False
