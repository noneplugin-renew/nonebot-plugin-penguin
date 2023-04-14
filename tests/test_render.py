import io
from pathlib import Path
from dataclasses import dataclass

import pytest
from PIL import Image
from nonebug import App
from nonebot import require


@pytest.mark.asyncio
async def test_render(app: App):
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import template_to_pic, template_to_html

    from nonebot_plugin_penguin.render import ItemIcon

    async def render():
        template_path = str(
            Path(__file__).parent.parent
            / "nonebot_plugin_penguin"
            / "render"
            / "templates"
        )
        print(template_path)
        template_name = "card.html"

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
            templates={
                "item_name": "测试",
                "item_icon_css": "background-image: url(./img/1.png);",
                "stages": stages,
                "all_stage": "10",
            },
            pages={
                "viewport": {"width": 440, "height": 300},
                "base_url": f"file://{template_path}",
            },
            wait=2,
        )

        a = Image.open(io.BytesIO(pic))
        a.show("template2pic.png")

    await render()
