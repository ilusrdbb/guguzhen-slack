import asyncio
import random

from aiohttp import ClientSession

from src.utils.log import log


async def get(url: str, headers: dict, session: ClientSession):
    try:
        res = await session.get(url=url, headers=headers, timeout=10)
        res_text = await res.text("utf-8", "ignore")
        if not res.status == 200:
            raise Exception(res_text)
        return res_text
    except Exception as e:
        log.info("%s 请求失败！" % url)
        log.info(e)
        return None

async def post_data(url: str, headers: dict, data: dict, session: ClientSession):
    await asyncio.sleep(random.random() * 1)
    try:
        res = await session.post(url=url, headers=headers, data=data, timeout=10)
        res_text = await res.text("utf-8", "ignore")
        if not res.status == 200:
            raise Exception(res_text)
        return res_text
    except Exception as e:
        log.info("%s 请求失败！" % url)
        log.info(e)
        return None