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

<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/owner/nonebot-plugin-penguin.svg" alt="license">
</a>

<a href="https://pypi.python.org/pypi/nonebot-plugin-penguin">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-penguin.svg" alt="pypi">
</a>

<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">

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

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| penguin_mirrior | 否 | io | 选择企鹅物流网站镜像为`国际(io)`或`国内(cn)` |
| penguin_show_count | 否 | 5 | 查询结果显示的条目数 |

## 🎉 使用

### 指令表

| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| `item <掉落物名称或别名(like: 双酮 紫薯)>` | 群员 | 否 | 群聊 | 查询该掉落物掉落率最高的若干个关卡 |
| `stage <关卡名(like: 1-7)` | 群员 | 否 | 群聊 | 查询该关卡掉落率最高的若干个掉落物 |
