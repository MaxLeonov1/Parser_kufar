import logging
import asyncio
from loader import *

from handlers.users import start,add,delete
from scripts import scheduler_update
from scripts.scheduler_update import update_scheduler


async def main():
    scheduler.start()
    update_scheduler()
    await dp.start_polling(bot,allowed_updates=dp.resolve_used_update_types())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())