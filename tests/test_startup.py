import respx
import pytest
from nonebug import App
from httpx import Response

from .utils import get_file


@pytest.mark.asyncio
@respx.mock
async def test_startup_run(app: App):
    from nonebot_plugin_penguin.config import plugin_config
    from nonebot_plugin_penguin.startup import (
        do_db_close,
        do_db_update,
        do_html_render_startup,
    )

    url1 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/items"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_items.json")))
    url2 = f"{plugin_config.penguin_site}/PenguinStats/api/v2/stages"
    url2_router = respx.get(url2)
    url2_router.mock(Response(200, text=get_file("request/fake_stages.json")))

    await do_db_update()
    await do_db_close()
    await do_html_render_startup()
