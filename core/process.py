import re

import aiohttp
from aiohttp import ClientSession

from module.battle import Battle
from module.shop import Shop
from module.wish import Wish
from utils import log, request


class Process(object):

    def __init__(self, user_setting: dict):
        self.user_setting = user_setting
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"]
        }
        self.url = "https://www.momozhen.com/fyg_index.php"

    async def run(self):
        if not self.user_setting["cookie"]:
            return
        jar = aiohttp.CookieJar(unsafe=True)
        conn = aiohttp.TCPConnector(ssl=False)
        async with aiohttp.ClientSession(connector=conn, trust_env=True, cookie_jar=jar) as session:
            user_bool = await self.get_user_info(session)
            if not user_bool:
                log.info("获取用户信息失败！")
                return
            await Shop(self.user_setting, session).run()
            await Wish(self.user_setting, session).run()
            await Battle(self.user_setting, session).run()

    async def get_user_info(self, session: ClientSession):
        res = await request.get(self.url, self.headers, session)
        if not res:
            return False
        # 获取safeid
        safeid_pattern = r'&safeid=([^"]+)"'
        match_safeid = re.findall(safeid_pattern, res)
        if not match_safeid:
            return False
        self.user_setting["safeid"] = match_safeid[0]
        # 获取用户名
        username_pattern = r'placeholder="([^"]+)'
        match_username = re.findall(username_pattern, res)
        if not match_username:
            return False
        self.user_setting["username"] = match_username[0]
        log.info(match_username[0] + " 开始摆烂...")
        return True