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
version = "1.2.1"


async def run(user_setting: dict):
    await Process(user_setting).run()

async def run_factory():
    await Process(None).factory_run()

if __name__ == '__main__':
    print("Version " + version)
    log.init_log()
    script.init_db()
    scheduler_flag = False
    # 显式创建并设置事件循环
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # 每隔一段时间刷新宝石工坊
    for setting in config.read():
        if setting["factory"] > 0:
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
            # 非定时出击 使用统一的事件循环执行任务
            loop.run_until_complete(run(setting))
    try:
        scheduler.start()
        # 使用显式创建的循环
        loop.run_forever()
    except Exception as e:
        log.info(str(e))
    finally:
        scheduler.shutdown()
