from aiohttp import ClientSession

from utils import log, request


class Shop(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.user_setting = user_setting
        self.shop_setting = user_setting["shop"]
        self.param = {
            "safeid": user_setting["safeid"],
            "c": ""
        }
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
            "cookie": user_setting["cookie"],
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        self.url = "https://www.momozhen.com/fyg_shop_click.php"

    async def run(self):
        # bvip日活
        log.info(self.user_setting["username"] + "开始领取BVIP打卡包...")
        self.param["c"] = "11"
        bvip_res = await request.post_data(self.url, self.headers, self.param, self.session)
        log.info(bvip_res)
        # svip日活
        log.info(self.user_setting["username"] + "开始领取SVIP打卡包...")
        self.param["c"] = "12"
        svip_res = await request.post_data(self.url, self.headers, self.param, self.session)
        log.info(svip_res)
        if self.shop_setting["sand_to_shell"]:
            # 星沙日活
            log.info(self.user_setting["username"] + "开始1星沙兑换10w贝壳...")
            self.param["c"] = "5"
            res = await request.post_data(self.url, self.headers, self.param, self.session)
            log.info(res)
        if self.shop_setting["crystal_to_shell"]:
            # 星晶日活
            log.info(self.user_setting["username"] + "开始1星晶兑换120w贝壳...")
            self.param["c"] = "6"
            res = await request.post_data(self.url, self.headers, self.param, self.session)
            log.info(res)