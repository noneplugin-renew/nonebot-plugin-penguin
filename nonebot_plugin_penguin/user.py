from typing import Union
from functools import partial

from nonebot.log import logger
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


def _gen_confirm_prompt(items: list, type_: str) -> str:
    prompt = f"请回复序号选择一个{str(type_)}：\n"
    key = "name" if type_ == "物品" else "code"
    for idx, candidate in enumerate(items):
        prompt += f"  {idx}. {candidate[key]}\n"
    return prompt


query = on_shell_command("penguin", aliases={"企鹅物流"}, parser=query_parser)


# 初始化处理，如果是错误退出则finish，否则转入下一个处理函数
@query.handle()
async def query_init(event: Union[V11Event, V12Event], state: T_State):
    parser_result = state["_args"]
    if isinstance(parser_result, ParserExit):
        await query.finish(parser_result.message)

    assert isinstance(parser_result, Namespace)
    logger.debug(f"get parser_result: {parser_result}")
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
        logger.debug(f"get items: {items}")
        if not items:
            await query.finish("该物品不存在")
        elif len(items) > 1:
            assert isinstance(items, list)
            logger.debug("找到多个物品")
            state["wait_confirm_item"] = (items, _gen_confirm_prompt(items, "物品"))
            state["sub_request"] = sub_request
            logger.debug("wait confirm item: {}".format(state["wait_confirm_item"]))
            logger.debug("sub request: {}".format(state["sub_request"]))
            await query.send("查询到多个物品，请选择")
        else:
            assert isinstance(items, list)
            item_id = items[0]["itemId"]
            full_request = sub_request(name=parser_result.names[0], ids=(item_id,))
            state["request"] = full_request
            logger.debug("already get full request: {}".format(state["request"]))

    elif parser_result.type == "stage" and len(parser_result.names) == 1:
        stages = await db.get_stage_id(parser_result.names[0].upper())
        logger.debug(f"get stages: {stages}")
        if not stages:
            await query.finish("该关卡不存在")
        elif len(stages) > 1:
            assert isinstance(stages, list)
            logger.debug("找到多个关卡")
            state["wait_confirm_stage"] = (stages, _gen_confirm_prompt(stages, "关卡"))
            state["sub_request"] = sub_request
            logger.debug("wait confirm stage: {}".format(state["wait_confirm_stage"]))
            logger.debug("sub request: {}".format(state["sub_request"]))
            await query.send("查询到多个关卡，请选择")
        else:
            assert isinstance(stages, list)
            stage_id = stages[0]["stageId"]
            full_request = sub_request(name=parser_result.names[0], ids=(stage_id,))
            state["request"] = full_request
            logger.debug("already get full request: {}".format(state["request"]))

    elif parser_result.type == "exact" and len(parser_result.names) == 2:
        stages = await db.get_stage_id(parser_result.names[0].upper())
        items = await db.get_item_id(parser_result.names[1])

        if not stages:
            await query.finish("关卡不存在")
        elif not items:
            await query.finish("物品不存在")
        elif len(items) > 1 or len(stages) > 1:
            assert isinstance(items, list)
            assert isinstance(stages, list)
            prompt = []
            if len(items) > 1:
                state["wait_confirm_item"] = (items, _gen_confirm_prompt(items, "物品"))
                prompt.append("物品")
                logger.debug("wait confirm item: {}".format(state["wait_confirm_item"]))
            if len(stages) > 1:
                state["wait_confirm_stage"] = (
                    stages,
                    _gen_confirm_prompt(stages, "关卡"),
                )
                prompt.append("关卡")
                logger.debug(
                    "wait confirm stage: {}".format(state["wait_confirm_stage"])
                )
            state["sub_request"] = sub_request
            logger.debug("sub request: {}".format(state["sub_request"]))
            await query.send("查询到多个" + "和".join(prompt) + "，请选择")
        else:
            assert isinstance(items, list)
            assert isinstance(stages, list)
            item_id = items[0]["itemId"]
            stage_id = stages[0]["stageId"]
            full_request = sub_request(
                name=" ".join(parser_result.names), ids=(stage_id, item_id)
            )
            state["request"] = full_request
            logger.debug("already get full request: {}".format(state["request"]))

    else:
        await query.finish("查询类型<type>与对应参数<ids>数量不匹配")


async def _need_confirm_item(state: T_State):
    if not state.get("wait_confirm_item", None):
        query.skip()
    elif not state.get("item_prompt_send", None):
        state["item_prompt_send"] = 1
        logger.debug("send item prompt...")
        await query.reject(state["wait_confirm_item"][1])


@query.handle([Depends(_need_confirm_item)])
async def query_confirm_item(event: Union[V11Event, V12Event], state: T_State):
    confirm_id = event.get_plaintext().strip()
    logger.debug(f"confirm item: {confirm_id}")
    if not confirm_id.isdigit():
        await query.reject("请输入数字序号")
    else:
        confirm_id = int(confirm_id)
        if confirm_id < 0 or confirm_id >= len(state["wait_confirm_item"][0]):
            logger.debug(f"confirm id:{confirm_id} out of range")
            await query.reject("序号超出范围")
        else:
            logger.debug(f"confirm id:{confirm_id} in range")
            items, _ = state["wait_confirm_item"]
            state["comfirm_item"] = items[confirm_id]
            state["wait_confirm_item"] = None
            logger.debug(f"confirm item: {state['comfirm_item']}")
            logger.debug(
                f"wait confirm item should empty: {state['wait_confirm_item']}"
            )

    logger.debug("confirm item done")


async def _need_confirm_stage(state: T_State):
    if not state.get("wait_confirm_stage", None):
        query.skip()
    elif not state.get("stage_prompt_send", None):
        state["stage_prompt_send"] = 1
        logger.debug("send stage prompt...")
        await query.reject(state["wait_confirm_stage"][1])


@query.handle([Depends(_need_confirm_stage)])
async def query_confirm_stage(event: Union[V11Event, V12Event], state: T_State):
    confirm_id = event.get_plaintext().strip()
    logger.debug(f"confirm stage: {confirm_id}")
    if not confirm_id.isdigit():
        await query.reject("请输入数字序号")
    else:
        confirm_id = int(confirm_id)
        if confirm_id < 0 or confirm_id >= len(state["wait_confirm_stage"][0]):
            logger.debug(f"confirm id:{confirm_id} out of range")
            await query.reject("序号超出范围")
        else:
            logger.debug(f"confirm id:{confirm_id} in range")
            stages, _ = state["wait_confirm_stage"]
            state["comfirm_stage"] = stages[confirm_id]
            state["wait_confirm_stage"] = None
            logger.debug(f"confirm stage: {state['comfirm_stage']}")
            logger.debug(
                f"wait confirm stage should empty: {state['wait_confirm_stage']}"
            )

    logger.debug("confirm stage done")


async def _is_all_confirmed(state: T_State):
    if state.get("wait_confirm_item", None) or state.get("wait_confirm_stage", None):
        await query.finish("流程错误!")


@query.handle([Depends(_is_all_confirmed)])
async def post_to_penguin(event: Union[V11Event, V12Event], state: T_State):
    logger.debug(f"state: {state}")

    if full_request := state.get("request", None):  # type: ignore
        assert isinstance(full_request, Request)
        logger.debug(f"is full request: {full_request.json(indent=4)}")
    else:
        logger.debug("is sub request")
        ids = []
        names = []
        if item := state.get("comfirm_item", None):
            logger.debug(f"has item: {item}")
            ids.append(item["itemId"])
            names.append(item["name"])
        if stage := state.get("comfirm_stage", None):
            logger.debug(f"has stage: {stage}")
            ids.append(stage["stageId"])
            names.append(stage["code"])

        logger.debug(f"ids: {ids}")
        logger.debug(f"names: {names}")
        sub_request = state["sub_request"]
        full_request: Request = sub_request(name=" ".join(names), ids=tuple(ids))
        logger.debug(f"created full request: {full_request.json(indent=4)}")

    try:
        result_pic_bytes = await render(full_request)
    except Exception as e:
        await query.finish(f"查询失败：{e}")
    else:
        url = f"{plugin_config.penguin_widget}/result/{full_request.server.upper()}/{full_request.type}"  # noqa: E501
        match full_request.type:
            case "item":
                url += f"/{full_request.ids[0]}"
            case "stage":
                url += f"/{full_request.ids[0]}"
            case "exact":
                url += f"/{full_request.ids[0]}/{full_request.ids[1]}"  # type: ignore
        url += f"?lang={full_request.lang}"

        await query.send("企鹅物流订单创建成功，正在配送中……")
        msg_builder = MessageFactory(Image(result_pic_bytes))  # type: ignore
        await msg_builder.send(at_sender=True)

        await query.finish(f"查询详情：{url}")
