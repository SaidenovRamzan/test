import asyncio
from aiogram import Bot,  Dispatcher, enums
from handlers import comand, orders, tg_chat


async def main() -> None:
    
    TOKEN = "6828045583:AAFF2kuNgxOlC7KSP6cQKXQjYkNke4RXu48"
    dp = Dispatcher()
    bot = Bot(TOKEN, parse_mode=enums.ParseMode.HTML)
    dp.include_router(orders.router)
    dp.include_router(comand.router)
    dp.include_router(tg_chat.router)
    await dp.start_polling(bot)
    
asyncio.run(main())

