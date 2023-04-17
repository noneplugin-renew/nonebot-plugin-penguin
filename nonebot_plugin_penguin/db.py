import time

from httpx import AsyncClient
from tinydb import Query, TinyDB

from .config import plugin_config

id_map = TinyDB(plugin_config.penguin_id_map)


async def id_map_init():
    if id_map.table("check").all():
        return
    id_map.table("check")
    id_map.table("items")
    id_map.table("stages")


# 反序列化时忽略不需要的字段
def _ignore_field(obj):
    return {k: v for k, v in obj.items() if k != "dropInfos"}


async def id_map_update():
    check_table = id_map.table("check")
    if last_update := check_table.get(Query().last_update.exists()):
        last_update_time: int = last_update["last_update"]
        if time.time() - last_update_time < 60 * 60 * 24:  # 小于1天就不用更新了
            return

    id_map.clear_cache()
    items_map = id_map.table("items")
    stages_map = id_map.table("stages")

    items_map.truncate()
    stages_map.truncate()

    async with AsyncClient() as clt:
        new_items = await clt.get(
            f"{plugin_config.penguin_site}/PenguinStats/api/v2/items"
        )
        new_stages = await clt.get(
            f"{plugin_config.penguin_site}/PenguinStats/api/v2/stages"
        )

    items_map.insert_multiple(new_items.json())
    stages_map.insert_multiple(
        new_stages.json(object_hook=_ignore_field)
    )  # 反序列化时忽略不需要的字段, 防止内存占用过大
    check_table.upsert({"last_update": int(time.time())}, Query().last_update.exists())


async def get_item_id(item_name: str):
    items_map = id_map.table("items")
    q = Query()
    if item := items_map.get(q.name_i18n.any([item_name])):
        return [item]
    else:
        items = items_map.search(q.alias.any([item_name]))
        return items


async def get_stage_id(stage_name: str):
    stages_map = id_map.table("stages")
    q = Query()
    return stages_map.get(q.code_i18n.any([stage_name]))
