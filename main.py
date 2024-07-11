import asyncio
import logging

from aiogram import Bot, Dispatcher
from config.config_file import load_config, Config
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers import other_handlers, user_handlers
from aiogram.fsm.storage.redis import RedisStorage, Redis
from keyboards.main_menu import set_main_menu

redis = Redis(host='localhost')
storage = storage = RedisStorage(redis=redis)
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )

    logger.info('Starting bot')

    config: Config = load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )

    dp = Dispatcher(storage=storage)

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
