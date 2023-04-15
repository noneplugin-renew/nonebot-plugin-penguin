from pathlib import Path

from nonebot import require

from ..model import Request
from ..request import Penguin
from ..trim import matrix_export
from ..config import plugin_config
from .item_sprite import Coord, ItemIcon

require("nonebot-plugin-htmlrender")
from nonebot_plugin_htmlrender import template_to_pic  # noqa: E402

_cache = None
template_path = Path(__file__).parent / "templates"


async def render(request: Request):
    penguin = Penguin()
    status_code = await penguin.fetch(request)
    if status_code != 200:
        return None

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
        case _:
            template_name = ""
            template_data = {}

    return await template_to_pic(
        template_name=template_name,
        template_path=template_path.as_posix(),
        templates=template_data,
        pages={
            "viewport": {"width": 440, "height": 300},
            "base_url": f"file://{template_path}",
        },
        wait=2,
    )
