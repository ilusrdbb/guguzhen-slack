import re

from aiohttp import ClientSession

from src.utils import request, config
from src.utils.log import log


class Factory(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.user_setting = user_setting
        self.sand_threshold = user_setting["factory"]
        if self.sand_threshold > 10:
            self.sand_threshold = 10
        self.param = {
            "f": "21"
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.url = "https://www.momozhen.com/fyg_read.php"

    async def run(self):
        # 刷新沙滩
        await request.get("https://www.momozhen.com/fyg_beach.php", self.headers, self.session)
        # 获取星沙
        res = await request.post_data(self.url, self.headers, self.param, self.session)
        if not res:
            return
        pattern = r'已开采<br>(.*?)星沙'
        match = re.findall(pattern, res)
        if not match:
            return
        now_sand = int(match[0])
        # 判断收工
        if now_sand >= self.sand_threshold:
            log.info(self.user_setting["username"] + "宝石工坊收工...")
            url = "https://www.momozhen.com/fyg_click.php"
            param = {
                "safeid": self.user_setting["safeid"],
                "c": "30"
            }
            complete_res = await request.post_data(url, self.headers, param, self.session)
            log.info(config.format_html(complete_res))
            # 收完工立即开工
            if "收工统计" in complete_res:
                start_res = await request.post_data(url, self.headers, param, self.session)
                log.info(start_res)