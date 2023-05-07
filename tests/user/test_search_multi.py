import pytest
from nonebug import App


@pytest.fixture
async def fake_pic() -> bytes:
    from nonebot_plugin_htmlrender import text_to_pic

    return await text_to_pic("test")


@pytest.mark.skip(reason="has bug")
@pytest.mark.asyncio
async def test_find_multi_item(chat_app: App, mocker, fake_pic):
    mocker.patch(
        "nonebot_plugin_penguin.render.table.html_to_pic_with_selector",
        return_value=b"test",
    )
    # from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot_plugin_saa import Image, MessageFactory

    # from nonebot.adapters.onebot.v11 import Adapter as V11Adapter
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
        fake_saa = MessageFactory(Image(b"test"))
        print(fake_saa)
        should_send_saa(
            ctx,
            fake_saa,
            bot,
            event=event_2_ok,
        )
        ctx.should_call_send(
            event_2_ok,
            f"查询详情：{plugin_config.penguin_widget}"
            + "/result/CN/item/2002"
            + "?lang=zh",
            True,
        )
        ctx.should_finished()
