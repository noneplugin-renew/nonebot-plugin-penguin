from nonebot import get_driver

from .db import id_map, id_map_init, id_map_update

driver = get_driver()


@driver.on_startup
def do_db_init():
    id_map_init()
    id_map_update()


@driver.on_shutdown
def do_db_close():
    id_map.close()
