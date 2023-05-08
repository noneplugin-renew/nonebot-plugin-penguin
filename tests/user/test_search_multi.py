import respx
import pytest
from nonebug import App
from httpx import Response

from ..utils import get_file


@pytest.mark.asyncio
async def test_find_multi_item(chat_app: App, mocker):
    fake_pic_data = b"test"
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=fake_pic_data,
    )
    from nonebot_plugin_saa import Image, MessageFactory
    from nonebot_plugin_saa.nonebug import should_send_saa
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin item 狗粮"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "查询到多个物品，请选择", True)
        ctx.should_call_send(
            event_1,
            "请回复序号选择一个物品：\n  "
            + "0. 基础作战记录\n  "
            + "1. 初级作战记录\n  "
            + "2. 中级作战记录\n  "
            + "3. 高级作战记录\n",
            True,
        )
        event_2_not_digit = fake_private_message_event(
            message=Message("a"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_not_digit)
        ctx.should_rejected()
        ctx.should_call_send(event_2_not_digit, "请输入数字序号", True)
        event_2_out_range = fake_private_message_event(
            message=Message("4"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_out_range)
        ctx.should_rejected()
        ctx.should_call_send(event_2_out_range, "序号超出范围", True)
        event_2_ok = fake_private_message_event(
            message=Message("1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_ok)
        ctx.should_call_send(event_2_ok, "企鹅物流订单创建成功，正在配送中……", True)
        fake_saa = MessageFactory(Image(fake_pic_data))
        should_send_saa(ctx, fake_saa, bot, event=event_2_ok, at_sender=True)
        ctx.should_call_send(
            event_2_ok,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/item/2002"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_multi_stage(chat_app: App, mocker):
    fake_pic_data = b"test"
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=fake_pic_data,
    )
    from nonebot_plugin_saa import Image, MessageFactory
    from nonebot_plugin_saa.nonebug import should_send_saa
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin stage WD-1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "查询到多个关卡，请选择", True)
        ctx.should_call_send(
            event_1,
            # fmt: off
            "请回复序号选择一个关卡：\n  "
            + "0. WD-1·复刻\n  "
            + "1. WD-1·首次\n  "
            + "2. WD-1·常驻\n",
            # fmt: on
            True,
        )
        event_2_not_digit = fake_private_message_event(
            message=Message("a"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_not_digit)
        ctx.should_rejected()
        ctx.should_call_send(event_2_not_digit, "请输入数字序号", True)
        event_2_out_range = fake_private_message_event(
            message=Message("99"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_out_range)
        ctx.should_rejected()
        ctx.should_call_send(event_2_out_range, "序号超出范围", True)
        event_2_ok = fake_private_message_event(
            message=Message("1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_ok)
        ctx.should_call_send(event_2_ok, "企鹅物流订单创建成功，正在配送中……", True)
        fake_saa = MessageFactory(Image(fake_pic_data))
        should_send_saa(ctx, fake_saa, bot, event=event_2_ok, at_sender=True)
        ctx.should_call_send(
            event_2_ok,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/stage/act18d0_01"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()


@pytest.mark.asyncio
@respx.mock
async def test_find_multi_exact(chat_app: App, mocker):
    fake_pic_data = b"test"
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=fake_pic_data,
    )
    from nonebot_plugin_saa import Image, MessageFactory
    from nonebot_plugin_saa.nonebug import should_send_saa
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.db import db
    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    from ..utils import fake_admin_user, fake_private_message_event

    url1 = f"{plugin_config.penguin_widget}/result/CN/exact/act18d0_01/2002"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_item_30014.html")))

    db.items_map

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin exact wd-1 狗粮"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "查询到多个物品和关卡，请选择", True)
        ctx.should_call_send(
            event_1,
            "请回复序号选择一个物品：\n  "
            + "0. 基础作战记录\n  "
            + "1. 初级作战记录\n  "
            + "2. 中级作战记录\n  "
            + "3. 高级作战记录\n",
            True,
        )
        event_2_item_ok = fake_private_message_event(
            message=Message("1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_item_ok)
        ctx.should_call_send(
            event_2_item_ok,
            # fmt: off
            "请回复序号选择一个关卡：\n  "
            + "0. WD-1·复刻\n  "
            + "1. WD-1·首次\n  "
            + "2. WD-1·常驻\n",
            # fmt: on
            True,
        )
        event_2_stage_ok = fake_private_message_event(
            message=Message("1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_2_stage_ok)
        ctx.should_call_send(event_2_stage_ok, "企鹅物流订单创建成功，正在配送中……", True)  # noqa: E501
        fake_saa = MessageFactory(Image(fake_pic_data))
        should_send_saa(ctx, fake_saa, bot, event=event_2_stage_ok, at_sender=True)
        ctx.should_call_send(
            event_2_stage_ok,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/exact/act18d0_01/2002"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()
