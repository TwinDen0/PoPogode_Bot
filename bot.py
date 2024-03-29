import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.utils import executor

from tgbot.config import load_config
from tgbot.filters.admin import AdminFilter
from tgbot.handlers.admin import register_admin
from tgbot.handlers.echo import register_echo
from tgbot.handlers.user_reg import register_user_reg
from tgbot.handlers.user_test import register_user_test
from tgbot.handlers.user_weather import register_user_weather
from tgbot.middlewares.environment import EnvironmentMiddleware

from tgbot.database import sqlite_db
from tgbot.services.scheduled import scheduled

logger = logging.getLogger(__name__)


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)


def register_all_handlers(dp):
    register_admin(dp)

    register_user_weather(dp)
    register_user_reg(dp)
    register_user_test(dp)

    register_echo(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    sqlite_db.sql_start()

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    register_all_filters(dp)
    register_all_handlers(dp)

    loop = asyncio.get_event_loop()
    # start
    try:
        # Вызываем функцию scheduled каждые 24 часа (86400 секунд)
        task_scheduled = scheduled(5, bot)

        task_polling = dp.start_polling()

        await asyncio.gather(task_scheduled, task_polling)

        executor.start_polling(dp, skip_updates=True)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
