import respx
import pytest
from nonebug import App
from httpx import Response

from .utils import get_json


@pytest.mark.asyncio
async def test_db_exist(app: App, tmpdir):
    with tmpdir.as_cwd():
        from nonebot_plugin_penguin.db import id_map

        assert not id_map.all()
        id_map.insert({"itemId": "1", "name_i18n": {"zh": "1"}, "spriteCoord": [1, 1]})
        assert id_map.all() == [
            {"itemId": "1", "name_i18n": {"zh": "1"}, "spriteCoord": [1, 1]}
        ]


@pytest.mark.asyncio
@respx.mock
async def test_db_update(app: App, tmpdir):
    with tmpdir.as_cwd():
        from nonebot_plugin_penguin.config import plugin_config
        from nonebot_plugin_penguin.db import id_map, id_map_update

        url1 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/items"
        url1_router = respx.get(url1)
        url1_router.mock(Response(200, text=get_json("request/fake_items.json")))
        url2 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/stages"
        url2_router = respx.get(url2)
        url2_router.mock(Response(200, text=get_json("request/fake_stages.json")))

        assert not id_map.all()
        await id_map_update()
        assert id_map.all()
