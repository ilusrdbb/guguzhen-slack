import hashlib
import re
import time
import uuid

from aiohttp import ClientSession

from module.analysis import Analysis
from module.clip import Clip
from utils import request, log


class Battle(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.battle_count = 0
        self.user_setting = user_setting
        self.param = {
            "safeid": user_setting["safeid"],
            "id": ""
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.url = "https://www.momozhen.com/fyg_v_intel.php"
        # battle mode
        self.battle_mode = user_setting["fight"]["battle_mode"]
        if self.battle_mode < 0:
            self.battle_mode = 0
        if self.battle_mode > 2:
            self.battle_mode = 2
        # 使用药水次数
        self.potion_count = user_setting["fight"]["use_potion"]
        if self.potion_count < 0:
            self.potion_count = 0
        if self.potion_count > 2:
            self.potion_count = 2

    async def run(self):
        if self.battle_count > 2 or self.potion_count < 1:
            return
        if self.battle_mode == 1:
            # 打野
            self.param["id"] = "1"
            log.info(self.user_setting["username"] + "开始打野...")
            await self.battle()
        if self.battle_mode == 2:
            # 打人
            self.param["id"] = "2"
            log.info(self.user_setting["username"] + "开始打人...")
            await self.battle()
        self.battle_count += 1
        # 翻牌
        await Clip(self.user_setting, self.session).run()
        # 使用体力药水
        if self.potion_count > 0:
            use_bool = await self.use_potion()
            if not use_bool:
                return
            self.potion_count -= 1
        await self.run()

    async def use_potion(self):
        log.info(self.user_setting["username"] + "消耗两瓶药水恢复体力...")
        param = {
            "safeid": self.user_setting["safeid"],
            "c": "13",
            "id": "2"
        }
        url = "https://www.momozhen.com/fyg_click.php"
        res = await request.post_data(url, self.headers, param, self.session)
        log.info(res)
        if res and res.startswith("可出击数已刷新"):
            return True
        else:
            return False

    async def battle(self):
        self.user_setting["battle"] = {
            "type": "attack"
        }
        # 获取当前段位
        await self.get_rank()
        res = await request.post_data(self.url, self.headers, self.param, self.session)
        if res and res.startswith('<div class="row">'):
            self.user_setting["battle"]["time"] = int(time.time() * 1000)
            # 模拟收割机生成id
            combined_string = res + str(self.user_setting["battle"]["time"])
            self.user_setting["battle"]["id"] = hashlib.md5(combined_string.encode('utf-8')).hexdigest()
            self.user_setting["log"] = res
            # 获取输赢
            if self.user_setting["username"] + " 获得了胜利！" in res:
                self.user_setting["battle"]["isWin"] = "true"
                log.info(self.user_setting["username"] + "赢了")
            elif "双方同归于尽！本场不计入胜负场次" in res:
                self.user_setting["battle"]["isWin"] = "0"
                log.info(self.user_setting["username"] + "平局")
            else:
                self.user_setting["battle"]["isWin"] = "false"
                log.info(self.user_setting["username"] + "输了")
            # 打人的记录转换为收割机格式并写数据库
            if self.param["id"] == "2":
                Analysis(self.user_setting).run()
            await self.battle()
        elif "请重试" in res:
            log.info(res)
            await self.battle()
        else:
            log.info(res)
            log.info(self.user_setting["username"] + "结束战斗")

    async def get_rank(self):
        url = "https://www.momozhen.com/fyg_read.php"
        param = {
            "f": "12"
        }
        res = await request.post_data(url, self.headers, param, self.session)
        if not res:
            return
        pattern = r'font-weight:900;">(.*?)</span><br>当前所在段位'
        matches = re.findall(pattern, res)
        if matches:
            self.user_setting["battle"]["rank"] = matches[0]