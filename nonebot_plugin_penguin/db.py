import time

from httpx import AsyncClient
from tinydb import Query, TinyDB

from .config import plugin_config


class DB:
    def __init__(self) -> None:
        self._do_init()

    def _do_init(self):
        self.id_map: TinyDB = TinyDB(plugin_config.penguin_id_map, encoding="utf-8")
        self.items_map = self.id_map.table("items")
        self.stages_map = self.id_map.table("stages")
        self.db_check = self.id_map.table("check")

    async def close(self):
        self.id_map.close()

    # 反序列化时忽略不需要的字段
    @staticmethod
    def _ignore_field(obj):
        return {k: v for k, v in obj.items() if k != "dropInfos"}

    async def id_map_update(self):
        if last_update := self.db_check.get(Query().last_update.exists()):
            last_update_time: int = last_update["last_update"]
            if time.time() - last_update_time < 60 * 60 * 24:  # 小于1天就不用更新了
                return

        self.id_map.clear_cache()

        self.items_map.truncate()
        self.stages_map.truncate()

        async with AsyncClient() as clt:
            new_items = await clt.get(
                f"{plugin_config.penguin_site}/PenguinStats/api/v2/items"
            )
            new_stages = await clt.get(
                f"{plugin_config.penguin_site}/PenguinStats/api/v2/stages"
            )

        self.items_map.insert_multiple(new_items.json())
        self.stages_map.insert_multiple(
            new_stages.json(object_hook=self._ignore_field)
        )  # 反序列化时忽略不需要的字段, 防止内存占用过大
        self.db_check.upsert(
            {"last_update": int(time.time())}, Query().last_update.exists()
        )

    async def get_item_id(self, item_name: str):
        q = Query()
        if item := self.items_map.get(
            q.name_i18n.test(lambda x: item_name in x.values())
        ):
            return [item]
        else:

            def _is_item_in_nested_alias(dict_values) -> bool:
                for values in dict_values:
                    if item_name in values:
                        return True
                return False

            items = self.items_map.search(
                q.alias.test(lambda x: _is_item_in_nested_alias(x.values()))
            )
            return items

    async def get_stage_id(self, stage_name: str):
        q = Query()
        return self.stages_map.get(q.code_i18n.test(lambda x: stage_name in x.values()))


db = DB()
