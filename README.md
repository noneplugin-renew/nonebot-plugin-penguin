<div align="center">
    <a href="https://v2.nonebot.dev/store">
        <img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
    </a>
    <br>
    <p>
        <img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText">
    </p>
</div>

<div align="center">

# nonebot-plugin-penguin

_✨ 向企鹅物流查询关卡掉落物数据 ✨_

[![license](https://img.shields.io/github/license/AzideCupric/nonebot-plugin-penguin)](https://github.com/AzideCupric/nonebot-plugin-penguin/blob/main/LICENSE)
[![action](https://img.shields.io/github/actions/workflow/status/AzideCupric/nonebot-plugin-penguin/test.yml?branch=main)](https://github.com/AzideCupric/nonebot-plugin-penguin/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/AzideCupric/nonebot-plugin-penguin/branch/main/graph/badge.svg?token=QCFIODJOOA)](https://codecov.io/gh/AzideCupric/nonebot-plugin-penguin)
[![python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/release/python-3100/)

</div>

## 📖 介绍

接入企鹅物流查询明日方舟关卡掉落物信息！

## 💿 安装

<details>
<summary> 
使用 nb-cli 安装
</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-penguin

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>
与仓库同步:

    pip install git+https://github.com/AzideCupric/nonebot-plugin-penguin.git

PyPi:

    pip install nonebot-plugin-penguin

</details>

<details>
<summary>poetry</summary>
与仓库同步:

    poetry add git+https://github.com/AzideCupric/nonebot-plugin-penguin.git

PyPi:

    poetry add nonebot-plugin-penguin

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_penguin"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|       配置项        | 必填 | 默认值 | 值类型/可选  |           说明           |
| :-----------------: | :--: | :----: | :----------: | :----------------------: |
|   penguin_mirrior   |  否  |   io   |   io / cn    |   选择企鹅物流网站镜像   |
| penguin_show_count  |  否  |   5    |  任意正整数  | 查询结果显示的最大条目数 |
| penguin_id_map_path |  否  |  <空>  | 任意存在目录 |  企鹅物流数据库存储路径  |

## 🎉 使用

### 指令

指令名: `penguin` 或者 `企鹅物流`

    格式:
    penguin [-h] {item,stage,exact} names [names ...] [-s {cn,kr,us,jp}] [-l {zh,ko,en,ja}] [-k {percentage,apPPR}] [-f {all,only_open,only_close}] [-t THRESHOLD] [-r]

    位置参数:
    {item,stage,exact}    查询类型
                            item: 按掉落物名查询
                            stage: 按关卡名查询,
                            exact: 精确查询(需指定关卡名和掉落物名)

    names                 关卡/掉落物名称或别名(H12-4 / 紫薯 / 固源岩)
                            type为exact时，关卡在前，空格隔开, 例如: 1-7 固源岩

    options:
    -h, --help              显示帮助

    -s {cn,kr,us,jp}, --server {cn,kr,us,jp}
                            游戏服务器选择, 默认为cn

    -l {zh,ko,en,ja}, --lang {zh,ko,en,ja}
                            生成回复时使用的语言, 默认为zh

    -k {percentage,apPPR}, --sort {percentage,apPPR}
                            排序方式, 默认为percentage
                            percentage: 掉落率
                            apPPR: 每个掉落物平均消耗理智

    -f {all,only_open,only_close}, --filter {all,only_open,only_close}
                            关卡过滤方式，默认为all

    -t THRESHOLD, --threshold THRESHOLD
                            掉落物过滤阈值, 默认超过100的样本数才会显示

    -r, --reverse         是否反转排序，建议使用apPPR排序时打开

例子:

1. 查询12-4的掉落物
   `penguin stage H12-4`
2. 查询紫薯的掉落关卡
   `penguin item 紫薯`
3. 查询12-4的掉落物, 且只显示开放的关卡
   `penguin stage 12-4 -f only_open`
4. 查询1-7的固源岩的掉落信息
   `penguin exact 1-7 固源岩`
5. 按apPPR(单件掉落物消耗理智)排序查询固源岩的掉落关卡(-r: apPPR越小越好)
   `penguin item 固源岩 -k apPPR -r`

\*请自行添加你给bot设置的命令前缀，如`/penguin`, `#penguin`

### ⚠️ 已知问题

0. 初次安装时，若之前没有使用过`nonebot-plugin-htmlrender`, 第一次使用时会开始安装浏览器，可能会比较~~非常~~慢
1. 可能是htmlrender或者网络的原因，有时候图片渲染会非常的慢，甚至超时，请重试

## 📝 ToDo

- 可以使用`penguin zone <活动名称>`查询一系列活动关卡
- 可以使用`penguin item/stage name1 name2 ...`批量查询
- 添加一个本地的缓存数据库，每周更新一次，减少网站访问频率，提高查询效率
