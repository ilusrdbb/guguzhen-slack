from aiohttp import ClientSession

from src.utils import request, config
from src.utils.log import log


class Wish(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.user_setting = user_setting
        self.wish_setting = user_setting["wish"]
        self.param = {
            "safeid": user_setting["safeid"],
            "c": "18",
            "id": "10"
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.url = "https://www.momozhen.com/fyg_click.php"

    async def run(self):
        if self.wish_setting:
            log.info(self.user_setting["username"] + "开始许愿...")
            res = await request.post_data(self.url, self.headers, self.param, self.session)
            log.info(config.format_html(res))