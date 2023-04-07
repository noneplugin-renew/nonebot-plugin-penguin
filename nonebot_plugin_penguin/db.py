from tinydb import  TinyDB, Query
from tinydb.table import Table, Document
from typing import Literal, Union
from model import Item, Stage, Request

T_DataModel = Union[Item, Stage, Request]
T_Table = Literal['item', 'stage', 'request']

class DB:

    tables: list[str] = ['item', 'stage', 'request']

    def __init__(self, path: str):
        self.db: TinyDB = TinyDB(path)
        # item_table 存储每个掉落物的itemId: str, name: str, alias: list[str]
        self.item_table: Table = self.db.table('item')
        # stage_table 存储每个关卡的stageId: str, code: str, apCost: int, minClearTime: int
        self.stage_table: Table = self.db.table('stage')
        # request_table 存储本次查询数据列表：stageId: str, itemId: str, times: int, quantity: int, stdDev: float, start: int, end:int|None
        self.request_table: Table = self.db.table('request')

    def add(self, table: T_Table, data: T_DataModel):
       self.db.table(table).insert(data.dict())

    def get_by_id(self, table: T_Table, data: T_DataModel) -> Document | None:
        """根据传入的data是否含有对应的*Id来获取对应的数据"""
        match data_dict := data.dict():
            case {'stageId': stageId, 'itemId': itemId}:
                return self.db.table(table).get((Query().stageId == stageId) & (Query().itemId == itemId))
            case {'itemId': itemId}:
                return self.db.table(table).get(Query().itemId == itemId)
            case {'stageId': stageId}:
                return self.db.table(table).get(Query().stageId == stageId)
            case _:
                raise ValueError('id不匹配')
            
    def get_by_item_name(self, name: str) -> Document | None:
        """从item_table中查询name字段，若name字段不匹配，尝试查询alias字段，均不匹配则抛出异常"""
        if item := self.item_table.get(Query().name == name):
            return item
        elif item:= self.item_table.search(Query().alias.any([name])):
            raise ValueError('未找到该物品')

    def delete(self, table: T_Table, data: T_DataModel) -> None:
        """根据传入的data是否含有对应的*Id来删除对应的数据"""
        if doc := self.get_by_id(table, data):
            self.db.table(table).remove(doc_ids=[doc.doc_id])
        else:
            raise ValueError('未找到该数据')

    def get_all_request(self) -> list[Document]:
        return self.request_table.all()

    def delete_all_request(self) -> None:
        self.request_table.truncate()

    def update_table(self, table: T_Table, data: T_DataModel) -> None:
        """更新指定table的记录"""
        if doc := self.get_by_id(table, data):
            self.db.table(table).update(data.dict(), doc_ids=[doc.doc_id])
        else:
            raise ValueError('未找到该数据')

    def close(self) -> None:
        self.db.close()