from nonebot.log import logger
from nonebot_plugin_apscheduler import scheduler

from .db import id_map_update


# 每周三周五 0点更新 id_map
@scheduler.scheduled_job("cron", day_of_week="3,5", hour=0)
async def update_item_and_stage_info():
    logger.info("Updating item and stage info...")
    await id_map_update()
