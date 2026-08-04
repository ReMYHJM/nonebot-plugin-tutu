import asyncio
import json
import random
from typing import List

import aiohttp
from nonebot import get_plugin_config, on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, MessageSegment
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata

from .config import Config


__plugin_meta__ = PluginMetadata(
    name="随机二次元图",
    description="从 yppp.net 获取随机二次元图片，支持多张合并发送",
    usage="/图图 [数量]",
    type="application",
    homepage="https://github.com/ReM-YHJM/nonebot-plugin-tutu",
    config=Config,
    supported_adapters={"~onebot.v11"},
)


tutu = on_command("图图", aliases={"随机图"})


_url_cache: List[str] = []
_cache_lock = asyncio.Lock()


# 固定 API 地址
API_PC = "https://api.yppp.net/pc.php?return=all"
API_PE = "https://api.yppp.net/pe.php?return=all"


async def _fetch_all_urls(config: Config) -> List[str]:
    """调用 return=all 获取全部图片 URL（去重）"""
    # 根据 orientation 选择接口
    if config.tutu_orientation == "pc":
        api_url = API_PC
    elif config.tutu_orientation == "pe":
        api_url = API_PE
    else:  # random
        api_url = API_PC if random.random() < 0.5 else API_PE

    headers = json.loads(config.tutu_headers_json)
    timeout = aiohttp.ClientTimeout(total=config.tutu_api_timeout)

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers, timeout=timeout) as resp:
            if resp.status != 200:
                raise Exception("批量获取失败")
            text = await resp.text()
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return list(set(lines))


async def _ensure_cache(config: Config) -> None:
    """确保缓存中有足够图片"""
    global _url_cache
    if len(_url_cache) >= config.tutu_max_count:
        return
    async with _cache_lock:
        if len(_url_cache) >= config.tutu_max_count:
            return
        new_urls = await _fetch_all_urls(config)
        if new_urls:
            random.shuffle(new_urls)
            _url_cache = new_urls


async def _get_random_urls(count: int, config: Config) -> List[str]:
    """从缓存中随机取出 count 个 URL（会从缓存中移除）"""
    global _url_cache
    if not _url_cache:
        await _ensure_cache(config)
    if len(_url_cache) < count:
        await _ensure_cache(config)

    if not _url_cache:
        return []

    if len(_url_cache) <= count:
        selected = _url_cache.copy()
        _url_cache.clear()
        return selected

    selected = random.sample(_url_cache, count)
    for url in selected:
        _url_cache.remove(url)
    return selected


@tutu.handle()
async def handle_tutu(bot: Bot, event: MessageEvent, args: Message = CommandArg()):
    config = get_plugin_config(Config)

    count = config.tutu_default_count
    arg_text = args.extract_plain_text().strip()
    if arg_text and arg_text.isdigit():
        count = int(arg_text)
        if count > config.tutu_max_count:
            count = config.tutu_max_count
        elif count < 1:
            count = 1

    try:
        urls = await _get_random_urls(count, config)
    except Exception:
        await tutu.finish("出现错误，肘飞坩埚")
        return

    if not urls:
        await tutu.finish("出现错误，肘飞坩埚")
        return

    # 所有图片合并为一条消息发送
    msgs = []
    for url in urls:
        msgs.append(MessageSegment.image(url))
    await tutu.finish(Message(msgs))
