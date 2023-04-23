import pytest
from nonebug import App


# @pytest.mark.skip(reason="TODO")
@pytest.mark.asyncio
async def test_single_choice(app: App):
    from nonebot.adapters.onebot.v11.bot import Bot
    from nonebot.adapters.onebot.v11.message import Message

    from nonebot_plugin_penguin.user import query

    from .utils import fake_admin_user, fake_private_message_event

    async with app.test_matcher(query) as ctx:
        bot = ctx.create_bot(base=Bot)
        event_1 = fake_private_message_event(
            message=Message("penguin"),
            sender=fake_admin_user,
            to_me=True,
        )
        ctx.receive_event(bot, event_1)
        ctx.should_call_send(event_1, "", True)
        ctx.should_finished()
