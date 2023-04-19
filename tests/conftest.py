import pytest
from nonebot import require
from nonebug import NONEBOT_INIT_KWARGS, App
from pytest_mock.plugin import MockerFixture


def pytest_configure(config: pytest.Config):
    config.stash[NONEBOT_INIT_KWARGS] = {
        "superusers": {"10001"},
        "command_start": {""},
        "log_level": "TRACE",
    }


@pytest.fixture
async def app(tmpdir, request: pytest.FixtureRequest, mocker: MockerFixture):
    with tmpdir.as_cwd():
        require("nonebot_plugin_htmlrender")
        require("nonebot_plugin_apscheduler")
        require("nonebot_plugin_saa")
        require("nonebot_plugin_penguin")
        from nonebot_plugin_htmlrender import shutdown_browser

        from nonebot_plugin_penguin.db import db

        db._do_init()

        yield App()

        await shutdown_browser()
        await db.close()
