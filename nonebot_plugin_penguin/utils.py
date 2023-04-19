from html.parser import HTMLParser

from nonebot.rule import ArgumentParser


class PenguinDataParser(HTMLParser):
    """解析id为penguinWidgetData的script标签"""

    def __init__(self):
        super().__init__()
        self.data: str = ""
        self.is_penguin_data = False

    def handle_starttag(self, tag, attrs):
        if tag == "script":
            for attr in attrs:
                if attr[0] == "id" and attr[1] == "penguinWidgetData":
                    self.is_penguin_data = True
                    break

    def handle_endtag(self, tag):
        if tag == "script":
            self.is_penguin_data = False

    def handle_data(self, data):
        if self.is_penguin_data:
            self.data = data


query_parser = ArgumentParser("query")
query_parser.add_argument(
    "type", type=str, choices=["item", "stage", "exact"], help="查询类型"
)
query_parser.add_argument(
    "names",
    type=str,
    nargs="+",
    help="关卡/掉落物名称或别名(H12-4 / 紫薯 / 固源岩), type为exact时，关卡在前，空格隔开, 例如: 1-7 固源岩",  # noqa: E501
)
query_parser.add_argument(
    "-s",
    "--server",
    type=str,
    required=False,
    default="cn",
    choices=["cn", "kr", "us", "jp"],
    help="游戏服务器",
)
query_parser.add_argument(
    "-l",
    "--lang",
    type=str,
    required=False,
    default="zh",
    choices=["zh", "ko", "en", "ja"],
    help="生成回复时使用的语言",
)
query_parser.add_argument(
    "-k",
    "--sort",
    type=str,
    required=False,
    default="percentage",
    choices=["percentage", "apPPR"],
    help="排序方式",
)
query_parser.add_argument(
    "-f",
    "--filter",
    type=str,
    required=False,
    default="all",
    choices=["all", "only_open", "only_close"],
    help="过滤方式",
)
query_parser.add_argument(
    "-t", "--threshold", type=int, required=False, default=100, help="过滤阈值"
)
query_parser.add_argument("-r", "--reverse", action="store_false", help="是否反转排序")
