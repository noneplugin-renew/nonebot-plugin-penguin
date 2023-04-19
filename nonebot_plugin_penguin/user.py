from typing import Union
from functools import partial

from nonebot.params import Depends
from nonebot.rule import Namespace
from nonebot.typing import T_State
from nonebot import on_shell_command
from nonebot.exception import ParserExit
from nonebot_plugin_saa import Image, MessageFactory
from nonebot.adapters.onebot.v11 import MessageEvent as V11Event
from nonebot.adapters.onebot.v12 import MessageEvent as V12Event

from .db import db
from .render import render
from .types import Request
from .utils import query_parser
from .config import plugin_config

# from nonebot_plugin_saa import MessageFactory, Image, Text

query = on_shell_command("query", aliases={"查询"}, parser=query_parser)


# 初始化处理，如果是错误退出则finish，否则转入下一个处理函数
@query.handle()
async def query_init(event: Union[V11Event, V12Event], state: T_State):
    parser_result = state["_args"]
    if isinstance(parser_result, ParserExit):
        await query.finish(parser_result.message)

    assert isinstance(parser_result, Namespace)

    # 固定Request的参数，现在还需要传入name，ids
    sub_request = partial(
        Request,
        server=parser_result.server,
        type=parser_result.type,
        lang=parser_result.lang,
        sort_by=parser_result.sort,
        filter_by=parser_result.filter,
        ignore_threshold=parser_result.threshold,
        reverse=parser_result.reverse,
    )

    if parser_result.type == "item" and len(parser_result.names) == 1:
        items = await db.get_item_id(parser_result.names[0])

        if not items:
            await query.finish("该物品不存在")
        elif len(items) > 1:
            state["wait_confirm"] = (items, sub_request)
            await query.pause("查询到多个物品，请选择")
        else:
            item_id = items[0]["itemId"]
            full_request = sub_request(name=parser_result.names[0], ids=(item_id,))
            state["request"] = full_request

    elif parser_result.type == "stage" and len(parser_result.names) == 1:
        stages = await db.get_stage_id(parser_result.names[0])

        if not stages:
            await query.finish("该关卡不存在")
        else:
            stage_id = stages["stageId"]
            full_request = sub_request(name=parser_result.names[0], ids=(stage_id,))
            state["request"] = full_request

    elif parser_result.type == "exact" and len(parser_result.names) == 2:
        stages = await db.get_stage_id(parser_result.names[0])
        items = await db.get_item_id(parser_result.names[1])

        if not stages or not items:
            await query.finish("关卡或物品不存在")
        elif len(items) > 1:
            state["wait_confirm"] = (items, sub_request)
            await query.pause("查询到多个物品，请选择")
        else:
            item_id = items[0]["itemId"]
            stage_id = stages["stageId"]
            full_request = sub_request(
                name=parser_result.names[0], ids=(stage_id, item_id)
            )
            state["request"] = full_request

    else:
        await query.finish("查询类型<type>与对应参数<ids>数量不匹配")


async def _multi_choice_confirm(state: T_State):
    if not state.get("wait_confirm", None):
        query.skip()

    wait_confirm_items = state["wait_confirm"][0]
    assert isinstance(wait_confirm_items, list)

    prompt = "请回复序号选择一个物品：\n"
    for idx, candidate in enumerate(wait_confirm_items):
        prompt += f"{idx}. {candidate['name']}\n"
    await query.send(prompt)


@query.receive("choice", [Depends(_multi_choice_confirm)])
async def confirm_receive(event: Union[V11Event, V12Event], state: T_State):
    confirm_id = event.get_plaintext().strip()
    if not confirm_id.isdigit():
        await query.reject_receive("请输入数字序号")
    else:
        confirm_id = int(confirm_id)
        if confirm_id < 0 or confirm_id >= len(state["wait_confirm"]):
            await query.reject_receive("序号超出范围")
        else:
            items, sub_request = state["wait_confirm"]
            item = items[confirm_id]
            full_request = sub_request(name=item["name"], ids=(item["itemId"],))
            state["request"] = full_request
            state["wait_confirm"] = None


@query.handle()
async def post_to_penguin(event: Union[V11Event, V12Event], state: T_State):
    request = state["request"]
    assert isinstance(request, Request)

    try:
        result_pic_bytes = await render(request)
    except Exception as e:
        await query.finish(f"查询失败：{e}")
    else:
        url = f"{plugin_config.penguin_widget}/result/{request.server.upper()}/{request.type}"  # noqa: E501
        match request.type:
            case "item":
                url += f"/{request.ids[0]}"
            case "stage":
                url += f"/{request.ids[0]}"
            case "exact":
                url += f"/{request.ids[0]}/{request.ids[1]}"  # type: ignore
        url += f"?lang={request.lang}"

        await query.send("企鹅物流订单创建成功，正在配送中……")
        msg_builder = MessageFactory(Image(result_pic_bytes))  # type: ignore
        await msg_builder.send(at_sender=True)

        await query.finish(f"查询详情：{url}")
