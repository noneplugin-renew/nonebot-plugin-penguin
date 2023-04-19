import pytest
from nonebug import App

from .utils import fake_admin_user, fake_private_message_event


@pytest.mark.asyncio
async def test_single_choice(app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query
    from nonebot_plugin_penguin.config import plugin_config

    async with app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("query"),
            sender=fake_admin_user,
            to_me=True,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(
            event_1, f"请访问: {plugin_config.penguin_site}auth/test_token", True
        )
        ctx.should_finished()
