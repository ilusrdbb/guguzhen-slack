import datetime
import json
import time

import yaml

from src.sqlite.battle import BattleData

export_setting = {}


def get_export_setting():
    with open('export.yaml', 'r', encoding='utf-8') as f:
        export_yaml = yaml.safe_load(f)
        export_setting["username"] = export_yaml["username"]
        # 转时间戳
        if export_yaml["start_date"]:
            start_datetime = datetime.datetime.strptime(export_yaml["start_date"] + ' 00:00:00.000',
                                                        "%Y-%m-%d %H:%M:%S.%f")
            start_timestamp = int(time.mktime(start_datetime.timetuple()) * 1000.0 + start_datetime.microsecond / 1000.0)
            export_setting["start_date"] = start_timestamp
        if export_yaml["end_date"]:
            end_datetime = datetime.datetime.strptime(export_yaml["end_date"] + ' 23:59:59.999',
                                                        "%Y-%m-%d %H:%M:%S.%f")
            end_timestamp = int(time.mktime(end_datetime.timetuple()) * 1000.0 + end_datetime.microsecond / 1000.0)
            export_setting["end_date"] = end_timestamp


if __name__ == '__main__':
    print("开始导出战斗记录...")
    # 获取配置
    get_export_setting()
    # 读数据库
    battle_data = BattleData(export_setting).select()
    for battle in battle_data:
        battle["damages"] = 0
        battle["invalids"] = []
        battle["attrs"] = battle["attrs"].split("|")
        battle["halos"] = battle["halos"].split("|")
        if battle["char"] == "野怪":
            battle["$types"] = {
                "armor": "undef",
                "attrs": "undef",
                "damages": "undef",
                "halos": "undef",
                "invalids": "arrayNonindexKeys",
                "time": "date",
                "weapon": "undef"
            }
            battle["armor"] = 0
            battle["attrs"] = 0
            battle["halos"] = 0
            battle["weapon"] = 0
            battle["type"] = "wild"
        else:
            battle["$types"] = {
                "attrs": "arrayNonindexKeys",
                "damages": "arrayNonindexKeys",
                "halos": "arrayNonindexKeys",
                "invalids": "arrayNonindexKeys",
                "time": "date"
            }
            battle["armor"] = "_void"
            battle["weapon"] = "_void"
        if battle["isWin"] == "true":
            battle["isWin"] = True
        if battle["isWin"] == "false":
            battle["isWin"] = False
        if battle["isWin"] == "0":
            battle["isWin"] = 0
    # 格式转换
    export_data = {
        "formatName": "dexie",
        "formatVersion": 1,
        "data": {
            "databaseName": "ggzharvester2",
            "databaseVersion": 1,
            "tables": [
                {
                    "name": "battleLog",
                    "schema": "id,time,username",
                    "rowCount": len(battle_data)
                }
            ],
            "data": [
                {
                    "tableName": "battleLog",
                    "inbound": True,
                    "rows": battle_data
                }
            ]
        }
    }
    # 导出
    if export_setting['username']:
        file_name = f"韭菜收割机历史数据_{export_setting['username']}_{str(time.time() * 1000)}.ggzjson"
    else:
        file_name = f"韭菜收割机历史数据_{str(time.time() * 1000)}.ggzjson"
    with open(file_name, "a", encoding="utf-8") as f:
        f.write(json.dumps(export_data))
    print("Press Enter to exit...")