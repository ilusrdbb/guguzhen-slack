import re

from aiohttp import ClientSession
from lxml import html

from utils import log, request


class Clip(object):

    def __init__(self, user_setting: dict, session: ClientSession):
        self.session = session
        self.user_setting = user_setting
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
            2: "默",
            3: "琳",
            4: "艾",
            5: "梦",
            6: "薇",
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
        log.info(self.user_setting["username"] + "开始翻牌...")
        # 获取透视
        refresh_res = await self.refresh()
        if not refresh_res:
            return
        if self.perspective_list:
            log.info(self.user_setting["username"] + "获取到透视：" + ",".join(self.perspective_list))
            # 翻开透视中的传说
            perspective_index = 1
            for perspective_card in self.perspective_list:
                if perspective_card == "传说":
                    self.param["id"] = perspective_index
                    await self.clip(False)
                perspective_index += 1
        # 起始翻牌位置
        self.param["id"] = len(self.perspective_list) + 1
        # 开翻
        await self.clip()

    async def refresh(self):
        url = "https://www.momozhen.com/fyg_read.php"
        param = {
            "f": "10"
        }
        res = await request.post_data(url, self.headers, param, self.session)
        if res and res.startswith('<div class="row fyg_tc">'):
            # 获取透视
            pattern = r'是“(.*?)”</p>'
            matches = re.findall(pattern, res)
            if matches:
                self.perspective_list = matches[0].split(",")
            else:
                # 没透视固定从左往右翻
                self.clip_setting = -1
            # 刷新翻牌结果
            if not self.analysis_clip_result(res):
                log.info(self.user_setting["username"] + "翻牌结果解析失败！结束翻牌")
                return False
            # 打印刷新后的翻牌结果
            print_info = ""
            for key, value in self.clip_info.items():
                print_info += f"{key}：{value} "
                if value > 2:
                    log.info(f"{self.user_setting['username']}翻牌结束！结果：{key}")
                    return False
            log.info(print_info)
            return True
        else:
            log.info(res)
            log.info(self.user_setting["username"] + "结束翻牌")
            return False

    def analysis_clip_result(self, res: str):
        clip_dom = html.fromstring(res)
        clip_xpath = "//button[contains(@class,'fyg_lh60')]//text()"
        read_list = clip_dom.xpath(clip_xpath)
        if read_list:
            # 初始化
            self.clip_info = {
                "幸运": 0,
                "稀有": 0,
                "史诗": 0,
                "传说": 0
            }
            for item in read_list:
                if self.clip_info.get(item) is None:
                    continue
                self.clip_info[item] += 1
            return True
        return False

    async def clip(self, loop: bool = True):
        res = await request.post_data(self.url, self.headers, self.param, self.session)
        if res == "" or res.startswith('<p class="fyg_f18">'):
            log.info(self.user_setting["username"] + "已翻开：" + self.position_map.get(self.param["id"]))
            # 刷新翻牌结果
            refresh_res = await self.refresh()
            if not refresh_res or not loop:
                return
            # 根据策略判断下张翻哪张
            await self.get_next_id()
            await self.clip()
        elif res == "该牌面已翻开":
            if loop:
                await self.get_next_id()
                await self.clip()
            return
        else:
            log.info(res)
            return

    async def get_next_id(self):
        if self.clip_setting == 0:
            for key, value in self.clip_info.items():
                # 判断是否有二传说 有就相当于无脑往下翻
                if key == "传说" and value > 1:
                    self.param["id"] += 1
                    return
            # 2幸运追求保底 但是优先级比2传说低
            for key, value in self.clip_info.items():
                if key == "幸运" and value > 1:
                    await self.guaranteed()
                    return
        elif self.clip_setting == 1:
            # 2幸运无脑追求保底
            for key, value in self.clip_info.items():
                if key == "幸运" and value > 1:
                    await self.guaranteed()
                    return
        self.param["id"] += 1

    async def guaranteed(self):
        # 把透视的加进目前已翻出的卡牌中
        merge_clip_info = {
            "幸运": self.clip_info["幸运"],
            "稀有": self.clip_info["稀有"],
            "史诗": self.clip_info["史诗"],
            "传说": self.clip_info["传说"]
        }
        for perspective in self.perspective_list:
            if perspective != "传说":
                merge_clip_info[perspective] += 1
        # 找出数量大于等于3的利益最大的透视卡
        guaranteed_key = ""
        for key, value in merge_clip_info.items():
            if value > 2 and key == "史诗":
                guaranteed_key = key
                break
            if value > 2 and key == "稀有":
                if not guaranteed_key:
                    guaranteed_key = key
        # 获取对应透视位置 并翻牌
        if guaranteed_key:
            perspective_index = 1
            for perspective in self.perspective_list:
                if perspective == guaranteed_key:
                    self.param["id"] = perspective_index
                    await self.clip(False)
                perspective_index += 1
            return
        self.param["id"] += 1

