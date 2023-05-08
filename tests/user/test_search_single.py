import respx
import pytest
from nonebug import App
from httpx import Response

from ..utils import get_file


@pytest.mark.asyncio
@respx.mock
async def test_find_single_item(chat_app: App, mocker):
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

    url1 = f"{plugin_config.penguin_widget}/result/CN/item/2004"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_item_2004.html")))

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin item 高级作战记录"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "企鹅物流订单创建成功，正在配送中……", True)
        fake_saa = MessageFactory(Image(fake_pic_data))
        should_send_saa(ctx, fake_saa, bot, event=event_1, at_sender=True)
        ctx.should_call_send(
            event_1,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/item/2004"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()


@pytest.mark.asyncio
@respx.mock
async def test_find_single_stage(chat_app: App, mocker):
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=b"test",
    )
    from nonebot_plugin_saa import Image, MessageFactory
    from nonebot_plugin_saa.nonebug import should_send_saa
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    from ..utils import fake_admin_user, fake_private_message_event

    url1 = f"{plugin_config.penguin_widget}/result/CN/stage/main_00-01"
    url1_router = respx.get(url1)
    url1_router.mock(Response(200, text=get_file("request/fake_stage_main_00-01.html")))

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin stage 0-1"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "企鹅物流订单创建成功，正在配送中……", True)
        fake_saa = MessageFactory(Image(b"test"))
        should_send_saa(ctx, fake_saa, bot, event=event_1, at_sender=True)
        ctx.should_call_send(
            event_1,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/stage/main_00-01"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()


@pytest.mark.asyncio
@respx.mock
async def test_find_single_exact(chat_app: App, mocker):
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=b"test",
    )
    from nonebot_plugin_saa import Image, MessageFactory
    from nonebot_plugin_saa.nonebug import should_send_saa
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    from ..utils import fake_admin_user, fake_private_message_event

    url1 = f"{plugin_config.penguin_widget}/result/CN/exact/main_00-01/2001"
    url1_router = respx.get(url1)
    url1_router.mock(
        Response(200, text=get_file("request/fake_exact_main_00-01_item_2001.html"))
    )

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot()
        event_1 = fake_private_message_event(
            message=Message("penguin exact 0-1 基础作战记录"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "企鹅物流订单创建成功，正在配送中……", True)
        fake_saa = MessageFactory(Image(b"test"))
        should_send_saa(ctx, fake_saa, bot, event=event_1, at_sender=True)
        ctx.should_call_send(
            event_1,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/exact/main_00-01/2001"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()
