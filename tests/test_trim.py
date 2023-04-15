from nonebug import App

from .utils import get_json


def test_export(app: App):
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_export
    from nonebot_plugin_penguin.types import Request, RenderByItem, RenderByStage

    penguin = Penguin()
    # item export
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))
    matrixs = penguin.matrix()
    request = Request(name="test", type="item", ids=("30014",), reverse=True)
    export = matrix_export(matrixs, request)
    assert len(export) == 11
    assert isinstance(export[1], RenderByItem)
    assert export[1].stage_name == "11-18"
    assert export[1].zone == "第十一章 (磨难)"
    assert export[1].percent == "5.45%"
    assert export[1].ap_cost == "3.85"
    assert export[1].rop_count == "3106"
    assert export[1].simple_count == "56995"
    assert export[1].open is True
    # stage export
    penguin2 = Penguin()
    penguin2.raw = ("stage", get_json("request/fake_stage_main_01-07.json"))
    matrixs2 = penguin2.matrix()
    request2 = Request(name="test", type="stage", ids=("main_01-07",), reverse=True)
    export2 = matrix_export(matrixs2, request2)
    assert len(export2) == 19
    assert isinstance(export2[1], RenderByStage)
    assert export2[1].item_name == "基础作战记录"
    assert export2[1].sprite_coord == [0, 0]
    assert export2[1].percent == "124.0%"
    assert export2[1].ap_cost == "0.05"
    assert export2[1].rop_count == "117270412"
    assert export2[1].simple_count == "94572340"


def test_sort(app: App):
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_sort

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()
    request = Request(
        name="test", type="item", ids=("30014",), reverse=True, sort_by="apPPR"
    )

    sort = matrix_sort(matrixs, request)
    assert len(sort) == 11
    assert sort[0].apPPR == 5.15
    assert sort[1].apPPR == 4.94
    assert sort[2].apPPR == 4.46
    assert sort[3].apPPR == 4.4
    assert sort[4].apPPR == 3.95
    assert sort[5].apPPR == 3.85
    assert sort[6].apPPR == 3.8
    assert sort[7].apPPR == 3.8
    assert sort[8].apPPR == 3.72
    assert sort[9].apPPR == 3.71
    assert sort[10].apPPR == 3.52

    request.sort_by = "percentage"
    request.reverse = False
    sort = matrix_sort(matrixs, request)
    assert len(sort) == 11
    assert sort[0].percentage == 4.04
    assert sort[1].percentage == 4.08
    assert sort[2].percentage == 4.25
    assert sort[3].percentage == 4.56
    assert sort[4].percentage == 4.74
    assert sort[5].percentage == 4.77
    assert sort[6].percentage == 4.84
    assert sort[7].percentage == 4.85
    assert sort[8].percentage == 5.11
    assert sort[9].percentage == 5.45
    assert sort[10].percentage == 5.53


def test_filter(app: App):
    from nonebot_plugin_penguin.types import Request
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_filter

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()
    request = Request(name="test", type="item", ids=("30014",), ignore_threshold=0)

    filter = matrix_filter(matrixs, request)
    assert len(filter) == 11
    for i in filter:
        assert i.end is None

    request.filter_by = "only_close"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 0

    request.filter_by = "all"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 11

    request.filter_by = "only_open"
    request.ignore_threshold = 1000
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 4
    for i in filter:
        assert i.end is None

    request.filter_by = "only_close"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 0
    for i in filter:
        assert i.end

    request.filter_by = "all"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 4

    request.filter_by = "only_open"
    request.ignore_threshold = 10000
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 0

    request.filter_by = "only_close"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 0

    request.filter_by = "all"
    filter = matrix_filter(matrixs, request)
    assert len(filter) == 0
