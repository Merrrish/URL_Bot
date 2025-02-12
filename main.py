import logging
import requests
import base64
import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from App.handlers import router

# Загружаем переменные окружения из .env
load_dotenv()

bot_token = os.getenv("BOT_TOKEN")
vt_token = os.getenv("VT_TOKEN")

# Проверяем, что токены загружены
if not bot_token or not vt_token:
    raise ValueError("❌ Один или оба токена не найдены! Проверь .env")

bot = Bot(token=bot_token)
dp = Dispatcher()

async def main():
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
