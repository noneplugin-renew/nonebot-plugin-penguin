from pydantic import BaseModel

class Item(BaseModel):
    itemId: str
    name: str
    alias: list[str]

class Stage(BaseModel):
    stageId: str
    code: str
    apCost: int
    minClearTime: int

class Request(BaseModel):
    stageId: str
    itemId: str
    times: int
    quantity: int
    stdDev: float
    start: int
    end: int|None
