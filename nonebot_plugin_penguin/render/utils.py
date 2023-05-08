from nonebot import require


async def startup_html_render():
    require("nonebot_plugin_htmlrender")
    from nonebot_plugin_htmlrender import text_to_pic

    await text_to_pic("Hello World!")
