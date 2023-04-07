
from typing import Literal

from nonebot import get_driver
from pydantic import BaseSettings


class PlugConfig(BaseSettings):

    penguin_mirrior: Literal["io", "cn"] = "io"

    class Config:
        extra = "ignore"

    def __init__(self):
        match self.penguin_mirrior:
            case "io":
                self.penguin_site: str = 'https://penguin-stats.io'
                self.penguin_cdn: str = 'https://penguin-stats.s3.amazonaws.com'
            case "cn":
                self.penguin_site: str = 'https://penguin-stats.cn'
                self.penguin_cdn: str = 'https://penguin.upyun.galvincdn.com'

global_config = get_driver().config
plugin_config = PlugConfig(**global_config.dict())