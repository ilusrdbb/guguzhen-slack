from aiohttp import ClientSession

from utils import log, request


class Clip(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.param = {
            "safeid": user_setting["safeid"],
            "c": "8",
            "id": 0
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
        # 透视
        self.perspective_list = []
        # 翻牌id映射
        self.position_map = {
            1: "舞",
            2: "",
            3: "",
            4: "",
            5: "",
            6: "",
            7: "伊",
            8: "冥",
            9: "命",
            10: "希",
            11: "霞",
            12: "绮"
        }
        # 翻牌统计
        self.clip_info = {
            "幸运": 0,
            "稀有": 0,
            "史诗": 0,
            "传说": 0
        }

    async def run(self):
        log.info("开始翻牌...")
        # todo 获取透视 翻开透视中的传说 刷新clip_info

        # 起始翻牌位置
        self.param["id"] = len(self.perspective_list) + 1
        # 开翻
        await self.clip()

    async def clip(self):
        res = await request.post_data(self.url, self.headers, self.param, self.session)
        if res and res.startswith(""):
            log.info("已翻开：" + self.position_map.get(self.param["id"]))
            # todo 刷新 打印翻牌统计
            # todo 根据策略判断翻哪张
            if self.clip_setting == 0:
                pass
            if self.clip_setting == 1:
                pass
            self.param["id"] = 114514
            # await self.clip()
        else:
            log.info(res)
            return

