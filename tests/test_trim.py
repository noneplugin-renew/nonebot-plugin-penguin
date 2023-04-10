from nonebug import App

from .utils import get_json


def test_export(app: App):
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_export

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()

    export = matrix_export(matrixs, "cn", "percentage", "only_open", True)
    assert len(export) == 11
    assert export[0].keys() == {
        "stage_name",
        "item_name",
        "zone_name",
        "sprite_coord",
        "percentage",
        "apPPR",
        "quantity",
        "time",
        "opening",
    }
    assert export[1]["stage_name"] == "11-18"
    assert export[1]["item_name"] == "提纯源岩"
    assert export[1]["zone_name"] == "第十一章 (磨难)"
    assert export[1]["sprite_coord"] == [1, 1]
    assert export[1]["percentage"] == "5.45%"
    assert export[1]["apPPR"] == 3.85
    assert export[1]["quantity"] == 3106
    assert export[1]["time"] == 56995
    assert export[1]["opening"] is True


def test_sort(app: App):
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_sort

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()

    sort = matrix_sort(matrixs, "apPPR", reverse=True)
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

    sort = matrix_sort(matrixs, "percentage")
    for i in sort:
        print(i.percentage)
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
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_filter

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()

    filter = matrix_filter(matrixs, "only_open", 0)
    assert len(filter) == 11
    for i in filter:
        assert i.end is None

    filter = matrix_filter(matrixs, "only_close", 0)
    assert len(filter) == 0

    filter = matrix_filter(matrixs, "all", 0)
    assert len(filter) == 11

    filter = matrix_filter(matrixs, "only_open", 1000)
    assert len(filter) == 4
    for i in filter:
        assert i.end is None

    filter = matrix_filter(matrixs, "only_close", 1000)
    assert len(filter) == 0
    for i in filter:
        assert i.end

    filter = matrix_filter(matrixs, "all", 1000)
    assert len(filter) == 4

    filter = matrix_filter(matrixs, "only_open", 10000)
    assert len(filter) == 0

    filter = matrix_filter(matrixs, "only_close", 10000)
    assert len(filter) == 0

    filter = matrix_filter(matrixs, "all", 10000)
    assert len(filter) == 0
