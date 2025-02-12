import requests
import base64
import os
from dotenv import load_dotenv
from aiogram import Bot, Router, types
from aiogram.filters import Command

# Загружаем переменные окружения
load_dotenv()
VT_TOKEN = os.getenv("VT_TOKEN")

# Проверяем, что токен загружен
if not VT_TOKEN:
    raise ValueError("❌ VT_TOKEN не найден! Проверь .env")

router = Router()

def check_url_with_virustotal(url):
    url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
    headers = {"x-apikey": VT_TOKEN}

    response = requests.get(f'https://www.virustotal.com/api/v3/urls/{url_id}', headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        analysis_stats = result['data']['attributes']['last_analysis_stats']
        if analysis_stats['malicious'] > 0:
            return {"safe": False, "message": "🚨 Обнаружена угроза!"}
        else:
            return {"safe": True, "message": "✅ Ссылка безопасна."}
    else:
        return {"safe": False, "message": f"⚠️ Ошибка API: {response.status_code}"}

@router.message(Command('start'))
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Пришлите мне URL, и я проверю его на наличие угроз.")

@router.message()
async def check_url(message: types.Message):
    url = message.text.strip()
    
    if not url.startswith(('http://', 'https://')):
        await message.reply("❌ Пожалуйста, пришлите действительный URL, начинающийся с http:// или https://")
        return

    await message.reply("🔍 Проверяю ссылку...")
    result = check_url_with_virustotal(url)
    await message.reply(result['message'])
