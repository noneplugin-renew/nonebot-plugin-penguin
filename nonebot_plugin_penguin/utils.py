from html.parser import HTMLParser


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
