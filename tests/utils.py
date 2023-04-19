import json
from pathlib import Path
from typing import Literal

from nonebot.adapters.onebot.v11.event import Sender
from nonebot.adapters.onebot.v11 import GroupMessageEvent, PrivateMessageEvent

path = Path(__file__).parent / "static"


def get_json(file_name: str):
    with (path / file_name).open("r", encoding="utf-8") as f:
        file_text = f.read()
        return json.loads(file_text)


def get_file(file_name: str):
    with (path / file_name).open("r", encoding="utf-8") as f:
        file_text = f.read()
        return file_text


def fake_group_message_event(**field) -> "GroupMessageEvent":
    from pydantic import create_model
    from nonebot.adapters.onebot.v11.event import Sender
    from nonebot.adapters.onebot.v11 import Message, GroupMessageEvent

    _Fake = create_model("_Fake", __base__=GroupMessageEvent)

    class FakeEvent(_Fake):
        time: int = 1000000
        self_id: int = 1
        post_type: Literal["message"] = "message"
        sub_type: str = "normal"
        user_id: int = 10
        message_type: Literal["group"] = "group"
        group_id: int = 10000
        message_id: int = 1
        message: Message = Message("test")
        raw_message: str = "test"
        font: int = 0
        sender: Sender = Sender(
            card="",
            nickname="test",
            role="member",
        )
        to_me: bool = False

        class Config:
            extra = "forbid"

    return FakeEvent(**field)


def fake_private_message_event(**field) -> "PrivateMessageEvent":
    from pydantic import create_model
    from nonebot.adapters.onebot.v11.event import Sender
    from nonebot.adapters.onebot.v11 import Message, PrivateMessageEvent

    _Fake = create_model("_Fake", __base__=PrivateMessageEvent)

    class FakeEvent(_Fake):
        time: int = 1000000
        self_id: int = 1
        post_type: Literal["message"] = "message"
        sub_type: str = "friend"
        user_id: int = 10
        message_type: Literal["private"] = "private"
        message_id: int = 1
        message: Message = Message("test")
        raw_message: str = "test"
        font: int = 0
        sender: Sender = Sender(nickname="test")
        to_me: bool = False

        class Config:
            extra = "forbid"

    return FakeEvent(**field)


fake_admin_user = Sender(nickname="test", role="admin")
fake_superuser = Sender(user_id=10001, nickname="superuser")
