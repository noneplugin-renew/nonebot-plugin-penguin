import pytest
from nonebug import App

from .utils import get_file


@pytest.mark.asyncio
async def test_penguin_data_parser(app: App):
    from nonebot_plugin_penguin.utils import PenguinDataParser

    parser = PenguinDataParser()
    raw_html = get_file("penguin_data.html")

    parser.feed(raw_html)
    assert '"query":{"stageId":"main_01-07","server":"CN"}' in parser.data
