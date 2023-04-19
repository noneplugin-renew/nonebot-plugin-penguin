from pathlib import Path

import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_schedule_exist(app: App):
    from apscheduler.job import Job
    from nonebot_plugin_apscheduler import scheduler

    jobs: list[Job] = scheduler.get_jobs()
    assert len(jobs) == 1
    update_job = jobs[0]
    assert update_job.name == "update_item_and_stage_info"


@pytest.mark.asyncio
async def test_schedule_run(app: App, tmp_path: Path):
    import io
    import contextlib

    from nonebot.log import logger, default_format

    from nonebot_plugin_penguin.schedule import update_item_and_stage_info

    log_path = tmp_path / "temp.log"

    logger.add(log_path, level="INFO", format=default_format, rotation="1 day")
    with contextlib.redirect_stderr(io.StringIO()) as f:
        await update_item_and_stage_info()

    with log_path.open("r", encoding="utf-8") as f:
        log = f.read()
        assert "Updating item and stage info..." in log
