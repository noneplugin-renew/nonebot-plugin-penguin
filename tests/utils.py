import json
from pathlib import Path

path = Path(__file__).parent / "static"


def get_json(file_name: str):
    with (path / file_name).open("r", encoding="utf-8") as f:
        file_text = f.read()
        return json.loads(file_text)


def get_file(file_name: str):
    with (path / file_name).open("r", encoding="utf-8") as f:
        file_text = f.read()
        return file_text
