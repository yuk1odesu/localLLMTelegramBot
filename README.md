# Telegram LLM Bot

Telegram-бот, который общается с локальной языковой моделью (LLM) через Ollama.

## Установка

1. Установите зависимости:
   ```bash
   pip install -r requirements.txt

2. Запустить Ollama:
   ```bash
   ollama serve

3. Загрузите модель:
   ```bash
   ollama pull llama3.1:8b-q4_K_M

4. Создайте .env файл:
   ```env
   ollama pull llama3.1:8b-q4_K_M

5. Запустите бота:
   ```bash
   python main.py

