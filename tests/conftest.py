import time
from typing import TypedDict

import pytest
from nonebot import require, get_driver
from nonebug import NONEBOT_INIT_KWARGS, App
from pytest_mock.plugin import MockerFixture
from nonebot.adapters.onebot.v11 import Adapter as OnebotV11Adapter

from .utils import get_json


class AppReq(TypedDict, total=False):
    dont_close_db: bool


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

        yield App()

        await shutdown_browser()

        if not param.get("dont_close_db", False):
            db.items_map.truncate()
            db.stages_map.truncate()
            db.db_check.truncate()


@pytest.fixture(scope="session", autouse=True)
def load_adapters(nonebug_init: None):
    driver = get_driver()
    driver.register_adapter(OnebotV11Adapter)


@pytest.fixture
async def chat_app(tmpdir, request: pytest.FixtureRequest, mocker: MockerFixture):
    with tmpdir.as_cwd():
        require("nonebot_plugin_penguin")
        from nonebot_plugin_htmlrender import shutdown_browser

        from nonebot_plugin_penguin.db import db

        db._do_init()

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
