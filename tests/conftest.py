from pathlib import Path

import pytest
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
    yield App()
