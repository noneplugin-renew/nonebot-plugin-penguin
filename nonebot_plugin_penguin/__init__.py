from nonebot import require
from nonebot.plugin import PluginMetadata

require("nonebot_plugin_apscheduler")
require("nonebot_plugin_saa")
require("nonebot_plugin_htmlrender")

from .config import PlugConfig  # noqa： E402
from . import (  # noqa： E402
    db,
    trim,
    user,
    types,
    utils,
    render,
    request,
    startup,
    schedule,
)

__all__ = [
    "render",
    "db",
    "request",
    "schedule",
    "startup",
    "trim",
    "user",
    "types",
    "utils",
]

__plugin_metadata__ = PluginMetadata(
    name="nonebot_plugin_penguin",
    description="使用nonebot2查询企鹅物流掉落物数据",
    usage="发送命令 `penguin -h` 查看帮助",
    type="application",
    homepage="https://github.com/AzideCupric/nonebot-plugin-penguin",
    config=PlugConfig,
    supported_adapters=None,
    extra={"authors": ["AzideCupric"], "license": "MIT"},
)
