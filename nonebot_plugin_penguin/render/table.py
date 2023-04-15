from pathlib import Path
from typing import Literal

from nonebot import require

from ..types import Request
from ..request import Penguin
from ..trim import matrix_export
from ..config import plugin_config
from .item_sprite import Coord, ItemIcon

template_path = Path(__file__).parent / "templates"


async def html_to_pic_with_selector(
    html: str,
    selector: str,
    wait: int = 0,
    template_path: str = "",
    type: Literal["jpeg", "png"] = "png",
    **pages,
) -> bytes:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import get_new_page

    if "file://" not in template_path:
        raise ValueError("template_path 应该为 file:///path/to/template")
    async with get_new_page(**pages) as page:
        await page.goto(template_path)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(wait)
        img_raw = await page.locator(selector).screenshot(
            type=type,
        )
    return img_raw


async def html_to_pic_with_selector(
    html: str,
    selector: str,
    wait: int = 0,
    template_path: str = "",
    type: Literal["jpeg", "png"] = "png",
    **pages,
) -> bytes:
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import get_new_page

    if not template_path and "file://" not in template_path:
        raise Exception("template_path 应该为 file:///path/to/template")
    async with get_new_page(**pages) as page:
        await page.goto(template_path)
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(wait)
        img_raw = await page.locator(selector).screenshot(
            type=type,
        )
    return img_raw


async def render(request: Request):
    penguin = Penguin()
    status_code = await penguin.fetch(request)
    if status_code != 200:
        return None

    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import template_to_html

    match request.type:
        case "item":
            trimed_data = matrix_export(penguin.matrix(), request)
            title = request.name.split()[0]
            sprite_coord = Coord(penguin.by_item_id(request.ids[0]).spriteCoord)
            template_name = "item_card.html"
            template_data = dict(
                item_name=title,
                item_icon_css=ItemIcon.style(sprite_coord),
                stages=trimed_data[: plugin_config.penguin_show_count],
                all_stage=len(trimed_data),
                sort_by=request.sort_by,
            )
        case "stage" | "exact":
            trimed_data = matrix_export(penguin.matrix(), request)
            title = request.name.split()[0]
            template_name = "stage_card.html"
            template_data = dict(
                stage_name=title,
                items=trimed_data[: plugin_config.penguin_show_count],
                all_item=len(trimed_data),
                sort_by=request.sort_by,
                icon=ItemIcon,
            )

    html = await template_to_html(
        template_name=template_name,
        template_path=template_path.as_posix(),
        **template_data,
    )

    # with open("temp_check.html", "w") as f:
    #     f.write(html)

    return await html_to_pic_with_selector(
        html=html,
        selector="body > div",
        template_path=f"file://{template_path.as_posix()}",
        viewport={"width": 1000, "height": 1000},
        base_url=f"file://{template_path}",
        wait=2,
    )
