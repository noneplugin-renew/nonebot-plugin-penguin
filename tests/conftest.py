from pathlib import Path

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
async def app(tmp_path: Path, request: pytest.FixtureRequest, mocker: MockerFixture):
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import shutdown_browser

    yield App()

    await shutdown_browser()
