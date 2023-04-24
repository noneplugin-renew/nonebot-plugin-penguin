import pytest
from nonebug import App


@pytest.mark.asyncio
async def test_command_help(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin"),
            sender=fake_admin_user,
            to_me=True,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(
            event_1,
            "usage: penguin [-h] [-s {cn,kr,us,jp}] [-l {zh,ko,en,ja}]\n"
            + "               [-k {percentage,apPPR}] [-f {all,only_open,only_close}]\n"
            + "               [-t THRESHOLD] [-r]\n"
            + "               {item,stage,exact} names [names ...]\n"
            + "penguin: error: the following arguments are required: type, names\n",
            True,
        )
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_item_404(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin item 超级作战记录"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "该物品不存在", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_stage_404(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin stage 99-99"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "该关卡不存在", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_exact_item_404(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin exact 99-99 初级作战记录"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "关卡不存在", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_exact_stage_404(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin exact 0-1 老猫金印"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "物品不存在", True)
        ctx.should_finished()


@pytest.mark.asyncio
async def test_find_too_many_err(chat_app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from ..utils import fake_admin_user, fake_private_message_event

    async with chat_app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin item 1-1 固源岩"),
            sender=fake_admin_user,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "查询类型<type>与对应参数<ids>数量不匹配", True)
        ctx.should_finished()
