from nonebot import get_driver

from .db import db

driver = get_driver()


@driver.on_startup
async def do_db_update():
    await db.id_map_update()


@driver.on_shutdown
async def do_db_close():
    db.close()
