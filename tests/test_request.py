import json

import respx
import pytest
from nonebug import App
from httpx import Response

from .utils import get_file, get_json


@pytest.mark.asyncio
@respx.mock
async def test_fetch(app: App):
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.config import plugin_config

    url1 = f"{plugin_config.penguin_widget}/result/CN/item/30014"
    url2 = f"{plugin_config.penguin_widget}/result/CN/stage/main_01-07"
    url3 = f"{plugin_config.penguin_widget}/result/CN/exact/main_01-07/30012"

    url1_router = respx.get(url1)
    url2_router = respx.get(url2)
    url3_router = respx.get(url3)

    url1_router.mock(Response(200, text=get_file("request/fake_item_30014.html")))
    url2_router.mock(Response(200, text=get_file("request/fake_stage_main_01-07.html")))
    url3_router.mock(
        Response(200, text=get_file("request/fake_exact_main_01-07_item_30012.html"))
    )

    penguin = Penguin()
    request1 = Request(name="test", type="item", ids=("30014",))
    await penguin.fetch(request1)
    assert url1_router.called
    assert url1_router.calls.last.response.status_code == 200
    assert url1_router.calls.last.request.url == url1
    assert "item" == penguin.raw[0]
    assert penguin.raw[1]["query"]["itemId"] == "30014"

    request2 = Request(name="test", type="stage", ids=("main_01-07",))
    await penguin.fetch(request2)
    assert url2_router.called
    assert url2_router.calls.last.response.status_code == 200
    assert url2_router.calls.last.request.url == url2
    assert "stage" == penguin.raw[0]
    assert penguin.raw[1]["query"]["stageId"] == "main_01-07"

    request3 = Request(name="test", type="exact", ids=("main_01-07", "30012"))
    res_code = await penguin.fetch(request3)
    assert url3_router.call_count == 1
    assert url3_router.calls.last.response.status_code == res_code
    assert url3_router.calls.last.request.url == url3
    assert "exact" == penguin.raw[0]
    assert penguin.raw[1]["query"]["stageId"] == "main_01-07"
    assert penguin.raw[1]["query"]["itemId"] == "30012"


@pytest.mark.asyncio
@respx.mock
async def test_all(app: App):
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.config import plugin_config

    url1 = f"{plugin_config.penguin_widget}/result/CN/item/30014"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_item_30014.html")))

    penguin = Penguin()
    request = Request(name="test", type="item", ids=("30014",))
    await penguin.fetch(request)
    assert "item" == penguin.all()[0]
    assert penguin.all()[1]["query"]["itemId"] == "30014"


def test_by_xx_id(app: App):
    from nonebot_plugin_penguin.request import Penguin

    penguin = Penguin()
    penguin.raw = ("item", json.loads(get_file("request/fake_penguin_raw.json")))

    assert penguin.by_item_id("30014").name_i18n["zh"] == "提纯源岩"
    assert penguin.by_item_id("30018").name_i18n["zh"] == "源岩碎块"

    assert penguin.by_stage_id("main_04-06").code_i18n["zh"] == "4-6"
    assert penguin.by_stage_id("act12side_07_perm").code_i18n["zh"] == "DH-7"

    assert penguin.by_zone_id("main_12_tough").zoneName_i18n["zh"] == "第十二章 (磨难)"
    assert (
        penguin.by_zone_id("permanent_sidestory_9_zone1").zoneName_i18n["zh"]
        == "多索雷斯假日・别传"
    )


def test_matrix(app: App):
    from nonebot_plugin_penguin.types import Matrix
    from nonebot_plugin_penguin.request import Penguin

    penguin = Penguin()
    penguin.raw = ("item", json.loads(get_file("request/fake_item_30014.json")))

    matrixs: list[Matrix] = penguin.matrix()

    assert len(matrixs) == 11
    matrix = matrixs[3]

    assert matrix.dict() == get_json("request/fake_matrix_result.json")


def test_translate(app: App):
    from nonebot_plugin_penguin.request import Penguin

    penguin = Penguin()
    penguin.raw = ("item", json.loads(get_file("request/fake_item_30014.json")))

    assert penguin.translate("cn", "item", "30014") == "提纯源岩"
    assert penguin.translate("cn", "stage", "act15side_07_perm") == "IW-7"
    trans = penguin.translate("cn", "zone", "permanent_sidestory_9_zone1")
    assert trans == "多索雷斯假日・别传"
    assert penguin.translate("cn", "matrix", "") == "暂不支持"
