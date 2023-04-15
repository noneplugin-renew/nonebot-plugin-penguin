import io
from pathlib import Path
from dataclasses import dataclass

import respx
import pytest
from PIL import Image
from flaky import flaky
from nonebug import App
from httpx import Response
from nonebot import require

from .utils import get_file


@pytest.mark.asyncio
@respx.mock
@flaky(max_runs=3, min_passes=1)
async def test_render_item(app: App):
    from nonebot_plugin_penguin.render import render
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.config import plugin_config

    url1 = f"{plugin_config.penguin_widget}/result/CN/item/30014"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_item_30014.html")))

    request = Request(name="test", type="item", ids=("30014",))

    pic_bytes = await render(request)
    assert pic_bytes
    assert pic_bytes.startswith(b"\x89PNG")
    # a = Image.open(io.BytesIO(pic_bytes))
    # a.show("template2pic.png")


@pytest.mark.asyncio
@respx.mock
@flaky(max_runs=3, min_passes=1)
async def test_render_stage(app: App):
    from nonebot_plugin_penguin.render import render
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.config import plugin_config

    url1 = f"{plugin_config.penguin_widget}/result/CN/stage/main_01-07"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_stage_main_01-07.html")))

    request = Request(name="test", type="stage", ids=("main_01-07",))

    pic_bytes = await render(request)
    assert pic_bytes
    assert pic_bytes.startswith(b"\x89PNG")
    # a = Image.open(io.BytesIO(pic_bytes))
    # a.show("template2pic.png")


@pytest.mark.asyncio
@respx.mock
async def test_error_fetch(app: App):
    from nonebot_plugin_penguin.render import render
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.config import plugin_config

    url1 = f"{plugin_config.penguin_widget}/result/CN/stage/main_01-07"
    url1_router = respx.get(url1)
    url1_router.mock(Response(500, text=get_file("request/fake_stage_main_01-07.html")))

    request = Request(name="test", type="stage", ids=("main_01-07",))
    assert await render(request) is None


@pytest.mark.asyncio
async def test_error_url(app: App):
    from nonebot_plugin_penguin.render.table import html_to_pic_with_selector

    with pytest.raises(ValueError):
        await html_to_pic_with_selector(
            html="<div></div>", selector="div", template_path="ftp://icu.996"
        )


@pytest.mark.skip(reason="这是一个测试htmlrender的测试，不需要自动运行")
@pytest.mark.asyncio
async def test_render(app: App):
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import template_to_pic, template_to_html

    from nonebot_plugin_penguin.render.item_sprite import ItemIcon

    async def render():
        template_path = str(
            Path(__file__).parent.parent
            / "nonebot_plugin_penguin"
            / "render"
            / "templates"
        )
        print(template_path)
        template_name = "item_card.html"

        @dataclass
        class Stage:
            name: str
            zone: str
            percent = "100%"
            ap_cost = "40"
            rop_count = "3"
            simple_count = "99"

        stages = [Stage(name=str(i) + "-1", zone=str(i) + "HH") for i in range(10)]

        t = {
            "item_name": "测试",
            "item_icon_css": ItemIcon.style((0, 0)),
            "stages": stages,
            "all_stage": "10",
            "sort_by": "apPPR",
        }

        html = await template_to_html(
            template_path=template_path, template_name=template_name, **t
        )
        with open("temp_html.html", "w", encoding="utf-8") as f:
            f.write(html)
        # 设置模板
        # 模板中本地资源地址需要相对于 base_url 或使用绝对路径
        pic = await template_to_pic(
            template_path=template_path,
            template_name=template_name,
            templates=t,
            pages={
                "viewport": {"width": 430, "height": 300},
                "base_url": f"file://{template_path}",
            },
            wait=2,
        )

        a = Image.open(io.BytesIO(pic))
        a.show("template2pic.png")

    await render()
