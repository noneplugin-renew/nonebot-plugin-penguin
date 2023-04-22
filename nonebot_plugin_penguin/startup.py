from nonebot import get_driver

from .db import db
from .render.utils import startup_html_render

driver = get_driver()


@driver.on_startup
async def do_db_update():
    await db.id_map_update()


@driver.on_startup
async def do_html_render_startup():
    await startup_html_render()


@driver.on_shutdown
async def do_db_close():
    await db.close()
