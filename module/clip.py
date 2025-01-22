from aiohttp import ClientSession


class Clip(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.param = {
            "safeid": user_setting["safeid"],
            "c": "8",
            "id": ""
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.url = "https://www.momozhen.com/fyg_click.php"
        # 翻牌策略
        self.clip_setting = user_setting["fight"]["flip_card_mode"]
        if self.clip_setting < 0:
            self.clip_setting = 0
        if self.clip_setting > 1:
            self.clip_setting = 1

    async def run(self):
        # todo 获取透视
        if self.clip_setting == 0:
            # todo 翻牌
            pass
        if self.clip_setting == 1:
            pass