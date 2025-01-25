import asyncio
from zoneinfo import ZoneInfo

from apscheduler.schedulers.background import BlockingScheduler

from core.process import Process
from sqlite import script
from utils import config, log

loop = asyncio.get_event_loop()
version = "1.0.0"


def run(user_setting: dict):
    log.init_log()
    loop.run_until_complete(Process(user_setting).run())
    log.remove_log()


if __name__ == '__main__':
    print("Version " + version)
    script.init_db()
    for setting in config.read():
        user_setting = setting
        scheduler_setting = user_setting["scheduler"]
        if scheduler_setting["enabled"]:
            scheduler = BlockingScheduler(timezone=ZoneInfo("Asia/Shanghai"))
            scheduler.add_job(
                run,
                "cron",
                hour=scheduler_setting["hour"],
                minute=scheduler_setting["minute"],
                misfire_grace_time=600,
                coalesce=True,
                max_instances=1,
                args=[user_setting]
            )
            scheduler.start()
        else:
            run()
    input("Press Enter to exit...")
