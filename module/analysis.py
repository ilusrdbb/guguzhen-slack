import re

from lxml import html

from sqlite.battle import BattleData


class Analysis(object):

    def __init__(self, user_setting: dict):
        self.user_setting = user_setting

    def run(self):
        log_dom = html.fromstring(self.user_setting["log"])
        battle_info = self.user_setting["battle"]
        # 获取对手信息
        enemy_info = self.get_enemy_info(log_dom)
        battle_info["enemyname"] = enemy_info.get("enemyname")
        battle_info["char"] = enemy_info.get("char")
        battle_info["charlevel"] = enemy_info.get("charlevel")
        # 获取箭头
        battle_info["attrs"] = self.get_attr_list(log_dom)
        # 获取光环
        battle_info["halos"] = self.get_halo_list(log_dom)
        # 获取装备
        gear_list = self.get_gear_list(log_dom)
        battle_info["weapon"] = gear_list[0]
        battle_info["armor"] = gear_list[2]
        # 写库
        BattleData(self.user_setting).insert()

    def get_enemy_info(self, log_dom):
        card_map = {
            '默': 'MO',
            '琳': 'LIN',
            '艾': 'AI',
            '梦': 'MENG',
            '薇': 'WEI',
            '冥': 'MING',
            '命': 'MIN',
            '伊': 'YI',
            '希': 'XI',
            '舞': 'WU',
            '霞': 'XIA',
            '雅': 'YA'
        }
        result_dict = {}
        info_xpath = "//div[contains(@class,'alert-info')]//span[contains(@class,'fyg_f18')]//text()"
        info_str = log_dom.xpath(info_xpath)
        if not info_str:
            return result_dict
        pattern = r'^(.*?)（(.*?) Lv\.(\d+)）$'
        match = re.match(pattern, info_str[0])
        if not match:
            return result_dict
        return {
            "enemyname": match.group(1),
            "char": card_map.get(match.group(2)),
            "charlevel": match.group(3)
        }

    def get_gear_list(self, log_dom):
        gear_map = {
            '探险者短杖': 'STAFF',
            '狂信者的荣誉之刃': 'BLADE',
            '反叛者的刺杀弓': 'ASSBOW',
            '幽梦匕首': 'DAGGER',
            '光辉法杖': 'WAND',
            '荆棘剑盾': 'SHIELD',
            '陨铁重剑': 'CLAYMORE',
            '饮血长枪': 'SPEAR',
            '探险者手套': 'GLOVES',
            '命师的传承手环': 'BRACELET',
            '秃鹫手套': 'VULTURE',
            '旅法师的灵光袍': 'CLOAK',
            '战线支撑者的荆棘重甲': 'THORN',
            '复苏木甲': 'WOOD',
            '挑战斗篷': 'CAPE',
            '探险者头巾': 'SCARF',
            '占星师的发饰': 'TIARA',
            '天使缎带': 'RIBBON',
            '海星戒指': 'RING',
            '噬魔戒指': 'DEVOUR',
            '探险者之剑': 'SWORD',
            '探险者短弓': 'BOW',
            '探险者铁甲': 'PLATE',
            '探险者皮甲': 'LEATHER',
            '探险者布甲': 'CLOTH',
            '萌爪耳钉': 'RIBBON',
            '荆棘盾剑': 'SHIELD',
            '饮血魔剑': 'SPEAR',
            '探险者手环': 'GLOVES',
            '秃鹫手环': 'VULTURE',
            '复苏战衣': 'WOOD',
            '探险者耳环': 'SCARF',
            '占星师的耳饰': 'TIARA',
            '彩金长剑': 'COLORFUL',
            '猎魔耳环': 'HUNT',
            '清澄长杖': 'LIMPIDWAND',
            '折光戒指': 'REFRACT',
            '凶神耳环': 'FIERCE'
        }
        gear_xpath = "//button[contains(@class,'fyg_colpzbg')]/@title"
        try:
            return [gear_map.get(log_dom.xpath(gear_xpath)[4]),
                    gear_map.get(log_dom.xpath(gear_xpath)[5]),
                    gear_map.get(log_dom.xpath(gear_xpath)[6]),
                    gear_map.get(log_dom.xpath(gear_xpath)[7])]
        except:
            return ["", "", "", ""]

    def get_halo_list(self, log_dom):
        result_list = []
        talent_map = {
            '启程之誓': 'SHI',
            '启程之心': 'XIN',
            '启程之风': 'FENG',
            '等级挑战': 'TIAO',
            '等级压制': 'YA',
            '破壁之心': 'BI',
            '破魔之心': 'MO',
            '复合护盾': 'DUN',
            '鲜血渴望': 'XUE',
            '削骨之痛': 'XIAO',
            '圣盾祝福': 'SHENG',
            '恶意抽奖': 'E',
            '伤口恶化': 'SHANG',
            '精神创伤': 'SHEN',
            '铁甲尖刺': 'CI',
            '忍无可忍': 'REN',
            '热血战魂': 'RE',
            '点到为止': 'DIAN',
            '午时已到': 'WU',
            '纸薄命硬': 'ZHI',
            '沸血之志': 'FEI',
            '波澜不惊': 'BO',
            '飓风之力': 'JU',
            '红蓝双刺': 'HONG',
            '荧光护盾': 'JUE',
            '后发制人': 'HOU',
            '钝化锋芒': 'DUNH',
            '自信回头': 'ZI',
            '不动如山': 'SHAN',
            '致命节奏': 'ZOU',
            '往返车票': 'PIAO',
            '天降花盆': 'PEN'
        }
        halo_xpath = "//div[contains(@class,'alert-info')]/div//div[contains(@class,'fyg_tr')]//text()"
        if not halo_xpath:
            return result_list
        halo_str = "".join(log_dom.xpath(halo_xpath))
        halo_list = re.findall("(?<=\\|).*?(?=\\|)", halo_str)
        for halo in halo_list:
            halo = halo.replace("|", "").replace("<br>", "")
            if halo:
                if halo == "启程之风" or halo == "等级挑战" or halo == "等级压制":
                    continue
                result_list.append(talent_map.get(halo))
        return result_list

    def get_attr_list(self, log_dom):
        result_list = []
        attr_xpath = "//div[contains(@class,'alert-info')]/div//span[contains(@class,'label-outline')]//i/@class"
        icon_list = log_dom.xpath(attr_xpath)
        if not icon_list:
            return result_list
        icon_str_list = [str(item) for item in icon_list]
        for icon in icon_str_list:
            if "double-angle-down" in icon:
                result_list.append("doubledown")
            if "icon-angle-down" in icon:
                result_list.append("down")
            if "icon-angle-up" in icon:
                result_list.append("up")
            if "double-angle-up" in icon:
                result_list.append("doubleup")
        return result_list
