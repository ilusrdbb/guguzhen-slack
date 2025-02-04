import asyncio
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BlockingScheduler

from core.process import Process
from sqlite import script
from utils import config, log

scheduler = BlockingScheduler(timezone=ZoneInfo("Asia/Shanghai"))
loop = asyncio.get_event_loop()
version = "1.1.0"


def run(user_setting: dict):
    log.init_log()
    loop.run_until_complete(Process(user_setting).run())
    log.remove_log()

def run_factory():
    log.init_log()
    loop.run_until_complete(Process(None).factory_run())
    log.remove_log()


if __name__ == '__main__':
    print("Version " + version)
    script.init_db()
    scheduler_flag = False
    # 每隔一段时间刷新宝石工坊
    for setting in config.read():
        if setting["factory"] >= 0:
            scheduler_flag = True
    if scheduler_flag:
        scheduler.add_job(
            run_factory,
            "interval",
            minutes=20,
            misfire_grace_time=60,
            coalesce=False,
            max_instances=1
        )
    # 每天其余的定时任务
    for setting in config.read():
        scheduler_setting = setting["scheduler"]
        if scheduler_setting["enabled"]:
            scheduler_flag = True
            scheduler.add_job(
                run,
                "cron",
                hour=scheduler_setting["hour"],
                minute=scheduler_setting["minute"],
                misfire_grace_time=600,
                coalesce=False,
                max_instances=1,
                args=[setting]
            )
        else:
            run(setting)
    if scheduler_flag:
        scheduler.start()
    else:
        input("Press Enter to exit...")
