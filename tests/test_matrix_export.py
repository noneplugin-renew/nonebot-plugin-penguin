import json

from nonebug import App

from .utils import get_json


def test_export(app: App):
    from nonebot_plugin_penguin.request import Penguin
    from nonebot_plugin_penguin.trim import matrix_export

    penguin = Penguin()
    penguin.raw = ("item", get_json("request/fake_item_30014.json"))

    matrixs = penguin.matrix()

    export = matrix_export(matrixs, "cn", "percentage", "only_open", True)
    print(json.dumps(export, indent=4, ensure_ascii=False))
