import asyncio
from zoneinfo import ZoneInfo

from apscheduler.executors.asyncio import AsyncIOExecutor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from src.core.process import Process
from src.sqlite import script
from src.utils import config
from src.utils.log import log

scheduler = AsyncIOScheduler(
    timezone=ZoneInfo("Asia/Shanghai"),
    executors={
        'asyncio': AsyncIOExecutor()
    }
)
loop = asyncio.get_event_loop()
version = "1.2.0"


async def run(user_setting: dict):
    await Process(user_setting).run()

async def run_factory():
    await Process(None).factory_run()

if __name__ == '__main__':
    print("Version " + version)
    log.init_log()
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
            max_instances=1,
            executor='asyncio'
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
                args=[setting],
                executor='asyncio'
            )
        else:
            asyncio.run(run(setting))
    if scheduler_flag:
        # 确保事件循环正确启动
        try:
            scheduler.start()
            asyncio.get_event_loop().run_forever()
        except (KeyboardInterrupt, SystemExit):
            pass
    else:
        input("Press Enter to exit...")
