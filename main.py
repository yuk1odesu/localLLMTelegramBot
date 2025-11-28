import asyncio
from collections import defaultdict
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import load_dotenv
import os

# Загружаем переменные из .env
load_dotenv()

# ВАЖНО: Токен берётся из .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не найден в .env файле")

# Хранилище контекста для каждого пользователя
user_contexts = defaultdict(list)

# Функция для получения ответа от локальной LLM
async def get_llm_response(user_id: int, prompt: str) -> str:
    import ollama

    # Добавляем сообщение пользователя в контекст
    user_contexts[user_id].append({'role': 'user', 'content': prompt})

    try:
        response = ollama.chat(
            model='llama3.1:8b-q4_K_M',  # Укажи нужную модель
            messages=user_contexts[user_id]
        )
        bot_response = response['message']['content']

        # Добавляем ответ бота в контекст
        user_contexts[user_id].append({'role': 'assistant', 'content': bot_response})

        # Ограничиваем длину истории (например, последние 20 сообщений)
        if len(user_contexts[user_id]) > 20:
            user_contexts[user_id] = user_contexts[user_id][-20:]

        return bot_response
    except Exception as e:
        return f"Ошибка при обращении к LLM: {str(e)}"

# Инициализация бота и диспетчера
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Обработчик команды /start
@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    user_id = message.from_user.id
    user_contexts[user_id].clear()  # Очищаем контекст при старте
    await message.answer("Привет! Я готов общаться с тобой с использованием локальной LLM. Пиши!")

# Обработчик текстовых сообщений
@dp.message()
async def handle_message(message: types.Message):
    user_id = message.from_user.id
    user_message = message.text

    print(f"Получено сообщение от {user_id}: {user_message}")

    # Получаем ответ от локальной LLM
    response = await get_llm_response(user_id, user_message)

    # Отправляем ответ пользователю
    await message.answer(response)

# Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
