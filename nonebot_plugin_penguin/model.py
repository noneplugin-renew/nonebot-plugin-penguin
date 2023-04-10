from pydantic import BaseModel


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
