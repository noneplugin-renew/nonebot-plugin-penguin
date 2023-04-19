import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_config(app: App):
    from nonebot_plugin_penguin.config import plugin_config

    assert plugin_config.penguin_mirrior == "io"
    assert plugin_config.penguin_show_count == 5

    assert plugin_config.penguin_site == "https://penguin-stats.io"
    assert plugin_config.penguin_cdn == "https://penguin-stats.s3.amazonaws.com"
    assert plugin_config.penguin_widget == "https://widget.penguin-stats.io"


@pytest.mark.asyncio
async def test_config_change(app: App, tmp_path):
    from nonebot_plugin_penguin.config import PlugConfig

    plugin_config = PlugConfig(
        penguin_mirrior="cn",
        penguin_show_count=7,
        penguin_id_map_path=(tmp_path / "penguin.db").as_posix(),
    )
    assert plugin_config.penguin_mirrior == "cn"
    assert plugin_config.penguin_show_count == 7

    assert plugin_config.penguin_site == "https://penguin-stats.cn"
    assert plugin_config.penguin_cdn == "https://penguin.upyun.galvincdn.com"
    assert plugin_config.penguin_widget == "https://widget.penguin-stats.cn"
    assert plugin_config.penguin_id_map == tmp_path / "penguin.db"
