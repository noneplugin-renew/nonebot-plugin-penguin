import respx
import pytest
import freezegun
from nonebug import App
from httpx import Response
from tinydb.table import Table
from tinydb import Query, TinyDB

from .utils import get_file


@pytest.mark.asyncio
async def test_db_exist(app: App, tmpdir):
    with tmpdir.as_cwd():
        from nonebot_plugin_penguin.db import db

        assert not db.id_map.all()
        assert not db.stages_map.all()

        db.stages_map.insert(
            {"itemId": "1", "name_i18n": {"zh": "1"}, "spriteCoord": [1, 1]}
        )
        assert db.stages_map.all() == [
            {"itemId": "1", "name_i18n": {"zh": "1"}, "spriteCoord": [1, 1]}
        ]


@freezegun.freeze_time("2022-02-02 02:02:02")
@pytest.mark.asyncio
@respx.mock
async def test_db_update_and_query(app: App, tmpdir):
    with tmpdir.as_cwd():
        from nonebot_plugin_penguin.db import db
        from nonebot_plugin_penguin.config import plugin_config

        url1 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/items"
        url1_router = respx.get(url1)
        url1_router.mock(Response(200, text=get_file("request/fake_items.json")))
        url2 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/stages"
        url2_router = respx.get(url2)
        url2_router.mock(Response(200, text=get_file("request/fake_stages.json")))

        assert not db.stages_map.all() and not db.items_map.all()
        await db.id_map_update()
        assert len(db.stages_map.all()) == 9
        assert len(db.items_map.all()) == 4
        # last_update 应该是 2022-02-02 02:02:02的时间戳(UTC+0)
        assert db.db_check.all() == [{"last_update": 1643767322}]
        # 改变last_update到半天前
        db.db_check.upsert(
            {"last_update": 1643767322 - 60 * 60 * 12}, Query().last_update.exists()
        )
        assert db.db_check.all() == [{"last_update": 1643767322 - 60 * 60 * 12}]
        # 再次更新，时间戳不会更新到最新
        await db.id_map_update()
        assert db.db_check.all() == [{"last_update": 1643767322 - 60 * 60 * 12}]

        item_use_name = await db.get_item_id("初级作战记录")
        assert len(item_use_name) == 1
        assert item_use_name[0]["itemType"] == "CARD_EXP"

        item_use_nickname = await db.get_item_id("狗粮")
        assert len(item_use_nickname) == 4

        item_exist_nai = await db.get_item_id("超级作战记录")
        assert not item_exist_nai

        stage_use_name = await db.get_stage_id("0-5")
        assert stage_use_name


@pytest.mark.asyncio
@pytest.mark.parametrize("app", [{"dont_close_db": True}], indirect=True)
async def test_db_close(app: App, tmpdir):
    with tmpdir.as_cwd():
        from nonebot_plugin_penguin.db import db

        assert isinstance(db.id_map, TinyDB)
        assert isinstance(db.stages_map, Table)
        assert isinstance(db.items_map, Table)
        assert isinstance(db.db_check, Table)
        await db.close()
        with pytest.raises(AssertionError):
            assert db.id_map is None
