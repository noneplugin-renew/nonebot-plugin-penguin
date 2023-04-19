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

<del>
<details>
<summary> 
使用 nb-cli 安装 (还没上传pypi喵)
</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-plugin-penguin

</details>
</del>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install git+https://github.com/AzideCupric/nonebot-plugin-penguin.git

</details>
<details>
<summary>pdm</summary>

    pdm add git+https://github.com/AzideCupric/nonebot-plugin-penguin.git

</details>
<details>
<summary>poetry</summary>

    poetry add git+https://github.com/AzideCupric/nonebot-plugin-penguin.git

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_penguin"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|       配置项       | 必填 | 默认值 |                     说明                     |
| :----------------: | :--: | :----: | :------------------------------------------: |
|  penguin_mirrior   |  否  |   io   | 选择企鹅物流网站镜像为`国际(io)`或`国内(cn)` |
| penguin_show_count |  否  |   5    |             查询结果显示的条目数             |

## 🎉 使用

### 指令

    格式:
    query [-h] {item,stage,exact} names [names ...] [-s {cn,kr,us,jp}] [-l {zh,ko,en,ja}] [-k {percentage,apPPR}] [-f {all,only_open,only_close}] [-t THRESHOLD] [-r]

    位置参数:
    {item,stage,exact}    查询类型
    names                 关卡/掉落物名称或别名(H12-4 / 紫薯 / 固源岩), type为exact时，关卡在前，空格隔开, 例如: 1-7 固源岩

    options:
    -h, --help              显示帮助
    -s {cn,kr,us,jp}, --server {cn,kr,us,jp}
                            游戏服务器选择, 默认为cn
    -l {zh,ko,en,ja}, --lang {zh,ko,en,ja}
                            生成回复时使用的语言, 默认为zh
    -k {percentage,apPPR}, --sort {percentage,apPPR}
                            排序方式, 默认为percentage, apPPR: 每个掉落物平均消耗理智
    -f {all,only_open,only_close}, --filter {all,only_open,only_close}
                            关卡过滤方式，默认为all
    -t THRESHOLD, --threshold THRESHOLD
                            掉落物过滤阈值, 默认超过100的样本数才会显示
    -r, --reverse         是否反转排序

例子:

1. 查询12-4的掉落物
   query stage H12-4
2. 查询紫薯的掉落关卡
   query item 紫薯
3. 查询12-4的掉落物, 且只显示开放的关卡
   query stage 12-4 -f only_open
4. 查询1-7的固源岩的掉落信息
   query exact 1-7 固源岩

\*请自行添加你给bot设置的命令前缀，如/query, #query

### :warning:已知问题

0. 初次安装时，若之前没有使用过`nonebot-plugin-htmlrender`, 第一次发送命令时会开始安装浏览器，可能会比较~~非常~~慢
1. stage/exact查询目前还无法区分别传，复刻，初次的活动关卡(如生于黑夜DM-X, 偷懒还没写 :dove::dove::dove:)
2. 发送查询命令之后，还需要再发一条无关消息才会开始渲染图片(会话控制问题，在改了在改了)
3. 如果使用物品别名进行查询(如：狗粮)，可能会提示出现多个结果，但需要发送一条无关消息后bot才会回复选项，之后才能回复相应序号(还是会话控制问题，在改了在改了)
