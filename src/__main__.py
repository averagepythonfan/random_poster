import asyncio
import logging
from aiogram import Dispatcher, Bot
from src.config import TOKEN
from src.handlers import router, commands_for_bot


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    
    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    dp.include_router(router=router)
    await bot.set_my_commands(commands=commands_for_bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())
