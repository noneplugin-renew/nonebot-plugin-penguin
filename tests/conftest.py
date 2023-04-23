import time
from typing import TypedDict

import pytest
from nonebot import require
from nonebug import NONEBOT_INIT_KWARGS, App
from pytest_mock.plugin import MockerFixture

from .utils import get_json


class AppReq(TypedDict, total=False):
    init_fake_db: bool


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "superusers": {"10001"},
        "command_start": {""},
        "log_level": "TRACE",
    }


@pytest.fixture
async def app(tmpdir, request: pytest.FixtureRequest, mocker: MockerFixture):
    with tmpdir.as_cwd():
        require("nonebot_plugin_penguin")
        from nonebot_plugin_htmlrender import shutdown_browser

        from nonebot_plugin_penguin.db import db

        param: AppReq = getattr(request, "param", AppReq())

        db._do_init()
        if param.get("init_fake_db", False):
            time_stamp = int(time.time())
            db.items_map.insert_multiple(get_json("request/fake_items.json"))
            db.stages_map.insert_multiple(get_json("request/fake_stages.json"))
            db.db_check.insert({"last_update": time_stamp})
            assert db.db_check.all() == [{"last_update": time_stamp}]

        yield App()

        await shutdown_browser()
        db.items_map.truncate()
        db.stages_map.truncate()
        db.db_check.truncate()
