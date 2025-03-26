from aiohttp import ClientSession

from src.utils import request, config
from src.utils.log import log


class Renew(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.user_setting = user_setting
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.param = {
            "iu": "2"
        }
        self.url = "https://www.momozhen.com/fyg_llpw_c.php"

    async def run(self):
        log.info(self.user_setting["username"] + "开始更新密钥...")
        res = await request.post_data(self.url, self.headers, self.param, self.session)
        if res and "ok" in res:
            log.info(self.user_setting["username"] + "更新密钥成功！")
        else:
            log.info(self.user_setting["username"] + "更新密钥失败！")