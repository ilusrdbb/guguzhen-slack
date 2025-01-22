import sqlite3


class BattleData(object):

    def __init__(self, user_setting: dict):
        self.user_setting = user_setting

    def select(self):
        # todo
        pass

    def insert(self):
        battle_info = self.user_setting["battle"]
        data_to_insert = (battle_info.get("id"), self.user_setting.get("username"), battle_info.get("enemyname"),
                          battle_info.get("char"), battle_info.get("charlevel"), battle_info.get("weapon"),
                          battle_info.get("armor"), "|".join(battle_info.get("attrs")), "|".join(battle_info.get("halos")),
                          self.user_setting.get("log"), battle_info.get("isWin"), battle_info.get("rank"),
                          battle_info.get("time"), battle_info.get("type"))
        conn = sqlite3.connect('slack.db')
        cursor = conn.cursor()
        sql = ("INSERT INTO battle_log (id, username, enemyname, char, charlevel, weapon, "
               "armor, attrs, halos, log, isWin, rank, time, type) "
               "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        cursor.execute(sql, data_to_insert)
        cursor.close()
        conn.commit()
        conn.close()