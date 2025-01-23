import datetime
import time

import yaml

from sqlite.battle import BattleData

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
    # todo 导出